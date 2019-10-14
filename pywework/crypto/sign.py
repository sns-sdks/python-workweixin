"""
    消息签名
"""
import hashlib
import logging

from pywework.error import ErrorCode

logger = logging.getLogger(__name__)


def get_sha1_signature(token: str, timestamp: str, nonce: str, encrypt: str):
    """
    生成 SHA1 签名
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
