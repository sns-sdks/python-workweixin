"""
    消息包体的校验
"""
import base64
import logging
import time

from typing import Tuple, Optional

from .sign import get_sha1_signature
from .msg_crypto import MsgCrypto

from pywework.error import WeWorkError, ErrorCode
from pywework.message.xml import xml_message

logger = logging.getLogger(__name__)


class MessageValidation:
    def __init__(self, token: str, aes_key: str, receive_id: str) -> None:
        """
        :param token: 签名 Token
        :param aes_key: AES 算法的秘钥
        :param receive_id: receive_id: corp_id 或者 suite_id
        https://work.weixin.qq.com/api/doc#90000/90139/90968/%E9%99%84%E6%B3%A8
        """
        try:
            self.key = base64.b64decode(aes_key + '=')
            assert len(self.key) == 32
        except Exception as e:
            logger.error(e)
            raise WeWorkError(ErrorCode.WXBizMsgCrypt_IllegalAesKey, 'EncodingAESKey invalid !')

        self.token = token
        self.receive_id = receive_id

    def verify_url(self, signature, timestamp, nonce, echo_str: str) -> Tuple[int, Optional[str]]:
        """
        验证URL有效性 的简化处理
        :param signature: 消息签名
        :param timestamp: 时间戳
        :param nonce: 随机串
        :param echo_str: 响应数据
        :return:
        """
        # 签名校验
        st, sign = get_sha1_signature(self.token, timestamp, nonce, echo_str)
        if st != 0:
            return st, None
        if sign != signature:
            return ErrorCode.WXBizMsgCrypt_ValidateSignature_Error, None

        # 解密获得消息内容
        mc = MsgCrypto(self.key)
        st, echo_str = mc.decipher(echo_str, self.receive_id)
        return st, echo_str

    def msg_build(self, reply: str, nonce: str, timestamp: str = None) -> Tuple[int, Optional[str]]:
        """
        打包消息体
        :param reply: 回复消息
        :param nonce: 随机字符串
        :param timestamp: 时间戳
        :return:
        """
        mc = MsgCrypto(self.key)

        st, cipher_text = mc.encipher(reply, self.receive_id)
        if st != 0:
            return st, None
        cipher_text = cipher_text.decode('utf-8')

        if timestamp is None:
            timestamp = str(int(time.time()))

        st, sign = get_sha1_signature(self.token, timestamp, nonce, cipher_text)
        if st != 0:
            return st, None

        respond_msg = xml_message.build_message(
            'respond',
            Encrypt=cipher_text,
            MsgSignature=sign,
            TimeStamp=timestamp,
            Nonce=nonce
        )
        return ErrorCode.WXBizMsgCrypt_OK, respond_msg

    def msg_parse(self, msg: str, signature: str, timestamp: str, nonce: str) -> Tuple[int, Optional[str]]:
        """
        原始消息解析
        :param msg: 消息 body
        :param signature: 签名
        :param timestamp: 时间戳
        :param nonce: 随机字符串
        :return:
        """
        try:
            msg_data = xml_message.parse_message(msg, respond=True)
            cipher_text = msg_data['Encrypt']
        except Exception as e:
            logger.error(e)
            return ErrorCode.WXBizMsgCrypt_ParseXml_Error, None

        st, sign = get_sha1_signature(self.token, timestamp, nonce, cipher_text)
        if st != 0:
            return st, None
        if sign != signature:
            return ErrorCode.WXBizMsgCrypt_ValidateSignature_Error, None

        mc = MsgCrypto(self.key)
        st, content = mc.decipher(cipher_text, self.receive_id)
        return st, content
