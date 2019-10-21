"""
    消息加密与解密
"""
import base64
import logging
import random
import socket
import struct

from Crypto.Cipher import AES

from pywework.error import ErrorCode
from .padding import PKCS7Padding

logger = logging.getLogger(__name__)


class MsgCrypto:
    """
    数据消息的加密与解密
    """

    def __init__(self, key: bytes) -> None:
        """
        :param key: 加密消息的 key
        """
        self.key = key
        self.mode = AES.MODE_CBC  # 加解密的模式

    def encipher(self, plain_text: str, receive_id: str):
        """
        对明文数据进行补位后加密
        :param plain_text: 需要加密的明文
        :param receive_id: corp_id 或者 suite_id
        https://work.weixin.qq.com/api/doc#90000/90139/90968/%E9%99%84%E6%B3%A8
        :return: 加密后的字符串
        """
        plain_text_bytes: bytes = plain_text.encode()
        # 拼接明文
        plain_text_bytes = b"".join(
            [
                self.get_random_str().encode(),  # 16字节 随机字符串
                struct.pack("I", socket.htonl(len(plain_text_bytes))),  # 4字节 消息长度
                plain_text_bytes,  # 消息内容
                receive_id.encode(),  # receive id
            ]
        )

        # 消息补位
        pkcs7 = PKCS7Padding()
        plain_text_bytes = pkcs7.encode(plain_text_bytes)

        # 数据加密
        crypter = AES.new(self.key, self.mode, self.key[:16])
        try:
            cipher_text = crypter.encrypt(plain_text_bytes)
            return ErrorCode.WXBizMsgCrypt_OK, base64.b64encode(cipher_text)
        except Exception as e:
            logger.error(e)
            return ErrorCode.WXBizMsgCrypt_EncryptAES_Error, None

    def decipher(self, cipher_text: str, receive_id: str):
        """
        对密文解密后移除补位
        :param cipher_text: 密文
        :param receive_id: corp_id 或者 suite_id
        https://work.weixin.qq.com/api/doc#90000/90139/90968/%E9%99%84%E6%B3%A8
        :return: 明文数据
        """
        crypter = AES.new(self.key, self.mode, self.key[:16])
        try:
            plain_text = crypter.decrypt(base64.b64decode(cipher_text))
        except Exception as e:
            logger.error(e)
            return ErrorCode.WXBizMsgCrypt_DecryptAES_Error, None

        # 移除补位
        pkcs7 = PKCS7Padding()
        plain_text = pkcs7.decode(plain_text)
        # 移除随机字符串
        plain_text = plain_text[16:]
        # 消息长度
        msg_len = socket.ntohl(struct.unpack("I", plain_text[:4])[0])
        # 消息内容
        msg_content = plain_text[4: msg_len + 4]
        # receive id
        from_received = plain_text[msg_len + 4:]

        # 判断 receive id
        if from_received.decode("utf-8") != receive_id:
            return ErrorCode.WXBizMsgCrypt_ValidateCorpid_Error, None

        return ErrorCode.WXBizMsgCrypt_OK, msg_content

    @staticmethod
    def get_random_str() -> str:
        """
        生成随机的16位字符串
        :return:
        """
        return str(random.randint(1000000000000000, 9999999999999999))
