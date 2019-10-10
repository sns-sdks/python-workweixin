"""
    Follow by https://github.com/sbzhu/weworkapi_python/blob/master/callback/WXBizMsgCrypt3.py
"""
import base64
import hashlib
import logging
import random
import socket
import struct
import time

import xml.etree.cElementTree as eT
from Crypto.Cipher import AES

from pywework.error import ErrorCode, WeWorkError
from pywework.utils import constant

logger = logging.getLogger(__name__)


class SHA1:
    """
    消息签名方法
    """

    @staticmethod
    def get_sha1_signature(token, timestamp, nonce, encrypt):
        """
        生成签名
        :param token: 生成签名需要的票据
        :param timestamp: 时间戳
        :param nonce: 随机字符串
        :param encrypt: 密文数据
        :return: 签名
        """
        try:
            params = [token, timestamp, nonce, encrypt]
            params.sort()
            sha1 = hashlib.sha1()
            sha1.update("".join(params).encode())
            return ErrorCode.WXBizMsgCrypt_OK, sha1.hexdigest()
        except Exception as e:
            logging.error(e)
            return ErrorCode.WXBizMsgCrypt_ComputeSignature_Error, None


class XMLParse:
    """
    提取消息中的密文以及生成回复消息的特定 xml 格式
    """

    AES_TEXT_RESPONSE_TEMPLATE = """
    <xml>
        <Encrypt><![CDATA[{msg_encrypt}]]></Encrypt>
        <MsgSignature><![CDATA[{msg_signature}]]></MsgSignature>
        <TimeStamp>{timestamp}</TimeStamp>
        <Nonce><![CDATA[{nonce}]]></Nonce>
    </xml>
    """

    @staticmethod
    def extract(xml_text):
        """
        提取 xml 消息中的密文数据
        :param xml_text: 待提取消息字符串
        :return: 加密后的消息体
        """
        try:
            xml_tree = eT.fromstring(xml_text)
            encrypt = xml_tree.find("Encrypt")
            return ErrorCode.WXBizMsgCrypt_OK, encrypt.text
        except Exception as e:
            logging.error(e)
            return ErrorCode.WXBizMsgCrypt_ParseXml_Error, None

    def generate(self, encrypt, signature, timestamp, nonce):
        """
        生成 xml 格式的消息体
        :param encrypt: 消息密文
        :param signature: 签名
        :param timestamp: 时间戳
        :param nonce: 随机字符串
        :return: xml 格式消息体
        """
        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE.format(
            msg_encrypt=encrypt, msg_signature=signature,
            timestamp=timestamp, nonce=nonce
        )
        return resp_xml


class DefaultDict(dict):
    def __missing__(self, key):
        return ''


class MessageXMLParse:
    """
    针对普通消息结构体的 解析 与 构建
    """
    SUPPORT_BUILD_TYPE = {
        'text': constant.XML_TEXT_STRUCT,
        'media': constant.XML_MEDIA_STRUCT,
        'link': constant.XML_LINK_STRUCT,
        'voice': constant.XML_VOICE_STRUCT,
        'video': constant.XML_VIDEO_STRUCT,
        'location': constant.XML_LOCATION_STRUCT
    }

    SUPPORT_PARSE_TYPE = {
        'text': constant.XML_TEXT_KEY,
        'media': constant.XML_MEDIA_KEY,
        'link': constant.XML_LINK_KEY,
        'voice': constant.XML_VOICE_KEY,
        'video': constant.XML_VIDEO_KEY,
        'location': constant.XML_LOCATION_KEY
    }

    def build_message(self, msg_type, **kwargs):
        if msg_type not in self.SUPPORT_BUILD_TYPE:
            raise WeWorkError(ErrorCode.NOT_SUPPORT_TYPE, f'Message type for {msg_type} not support to build.')
        base_info = self.SUPPORT_BUILD_TYPE[msg_type]
        return base_info.format_map(DefaultDict(kwargs))

    def parse_message(self, message):
        xml_tree = eT.fromstring(message)
        msg_type = xml_tree.find('MsgType').text
        if msg_type not in self.SUPPORT_PARSE_TYPE:
            raise WeWorkError(ErrorCode.NOT_SUPPORT_TYPE, f'Message type for {msg_type} not support to parse.')
        res = {}
        for key in self.SUPPORT_PARSE_TYPE[msg_type]:
            res[key] = xml_tree.find(key).text
        return res


class PKCS7Encoder:
    """ 提供基于 PKCS7 算法的加解密接口 """
    BLOCK_SIZE = 32

    def encode(self, text):
        """
        对需要加密的明文数据进行补位
        :param text: 明文数据
        :return: 补全的明文
        """
        text_length = len(text)
        amount_to_pad = self.BLOCK_SIZE - (text_length % self.BLOCK_SIZE)
        if amount_to_pad == 0:
            amount_to_pad = self.BLOCK_SIZE
        pad = chr(amount_to_pad)
        return text + (pad * amount_to_pad).encode()

    def decode(self, decrypted):
        """
        删除解密后的补位字符
        :param decrypted: 解密后的明文
        :return: 移除补位字符后的明文
        """
        pad = decrypted[-1]
        if pad < 1 or pad > self.BLOCK_SIZE:
            pad = 0
        return decrypted[:-pad]


class MsgCrypt:
    """ 接收与推送到企业微信的消息的加解密 """

    def __init__(self, key):
        """
        :param key:
        """
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text, received):
        """
        对明文数据加密
        :param text: 需要加密的明文数据
        :param received:
        :return:
        """
        # 16 位随机字符串添加
        text = text.encode()
        text = self.get_random_str() + struct.pack("I", socket.htonl(len(text))) + text + received.encode()

        # 自定义字符填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)

        # 加密数据
        crypter = AES.new(self.key, self.mode, self.key[:16])

        try:
            cipher = crypter.encrypt(text)
            return ErrorCode.WXBizMsgCrypt_OK, base64.b64encode(cipher)
        except Exception as e:
            logger.error(e)
            return ErrorCode.WXBizMsgCrypt_EncryptAES_Error, None

    def decrypt(self, text, received):
        """
        对密文进行解密，并将解密后的明文字符串进行补位移除
        :param text: 密文
        :param received:
        :return:
        """
        # 解密
        try:
            crypter = AES.new(self.key, self.mode, self.key[:16])
            plain_text = crypter.decrypt(base64.b64decode(text))
        except Exception as e:
            logger.error(e)
            return ErrorCode.WXBizMsgCrypt_DecryptAES_Error, None

        try:
            pad = plain_text[-1]
            # 移除补位字符串和前16位随机字符串
            content = plain_text[16:-pad]

            xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
            xml_content = content[4: xml_len + 4]
            from_received = content[xml_len + 4:]
        except Exception as e:
            logger.error(e)
            return ErrorCode.WXBizMsgCrypt_IllegalBuffer, None

        if from_received.decode('utf-8') != received:
            return ErrorCode.WXBizMsgCrypt_ValidateCorpid_Error, None

        return 0, xml_content

    @staticmethod
    def get_random_str():
        """
        随机 16 位 字符串
        :return:
        """
        return str(random.randint(1000000000000000, 9999999999999999)).encode()


class Packet:
    def __init__(self, token, aes_key, received):
        try:
            self.key = base64.b64decode(aes_key + "=")
            assert len(self.key) == 32
        except Exception as e:
            logger.error(e)
            raise WeWorkError(ErrorCode.WXBizMsgCrypt_IllegalAesKey, 'EncodingAESKey invalid !')
        self.token = token
        self.received = received
        self.msg_xml_parser = MessageXMLParse()

    def verify_url(self, signature, timestamp, nonce, echo_str):
        """
        验证 服务端 提供的 url
        :param signature: 签名
        :param timestamp: 时间戳
        :param nonce: 随机串
        :param echo_str: url 包含的响应串
        :return:
        """
        sha1 = SHA1()
        ret, sign = sha1.get_sha1_signature(self.token, timestamp, nonce, echo_str)
        if ret != 0:
            return ret, None
        if sign != signature:
            return ErrorCode.WXBizMsgCrypt_ValidateSignature_Error, None

        mc = MsgCrypt(self.key)

        ret, echo_str = mc.decrypt(echo_str, self.received)
        return ret, echo_str

    def encrypt_msg(self, reply, nonce, timestamp=None):
        """
        回复用户的消息进行加密后打包
        :param reply: 需要回复的消息
        :param nonce: 随机字符串
        :param timestamp: 时间戳
        :return:
        """
        mc = MsgCrypt(self.key)
        ret, encrypt = mc.encrypt(reply, self.received)
        encrypt = encrypt.decode('utf-8')

        if ret != 0:
            return ret, None
        if timestamp is None:
            timestamp = str(int(time.time()))

        sha1 = SHA1()
        ret, sign = sha1.get_sha1_signature(self.token, timestamp, nonce, encrypt)
        if ret != 0:
            return ret, None
        xml_parse = XMLParse()
        return ret, xml_parse.generate(encrypt, sign, timestamp, nonce)

    def decrypt_msg(self, msg, signature, timestamp, nonce):
        """
        验证消息，并获取到解密后的明文
        :param msg: 密文数据
        :param signature: 签名
        :param timestamp: 时间戳
        :param nonce: 随机字符串
        :return: 解密后的字符串
        """
        xml_parse = XMLParse()
        ret, encrypt = xml_parse.extract(msg)
        if ret != 0:
            return ret, None

        sha1 = SHA1()
        ret, sign = sha1.get_sha1_signature(self.token, timestamp, nonce, encrypt)
        if ret != 0:
            return ret, None
        if sign != signature:
            return ErrorCode.WXBizMsgCrypt_ValidateSignature_Error, None
        mc = MsgCrypt(self.key)
        ret, xml_content = mc.decrypt(encrypt, self.received)
        return ret, xml_content
