""" error """


class ErrorCode:
    NOT_SUPPORT_METHOD = 11001
    NOT_SUPPORT_TYPE = 11002
    INVALID_PARAM = 11003
    MISSION_PARAM = 11004

    # 用于 接收消息的验证
    WXBizMsgCrypt_OK = 0
    WXBizMsgCrypt_ValidateSignature_Error = -40001
    WXBizMsgCrypt_ParseXml_Error = -40002
    WXBizMsgCrypt_ComputeSignature_Error = -40003
    WXBizMsgCrypt_IllegalAesKey = -40004
    WXBizMsgCrypt_ValidateCorpid_Error = -40005
    WXBizMsgCrypt_EncryptAES_Error = -40006
    WXBizMsgCrypt_DecryptAES_Error = -40007
    WXBizMsgCrypt_IllegalBuffer = -40008
    WXBizMsgCrypt_EncodeBase64_Error = -40009
    WXBizMsgCrypt_DecodeBase64_Error = -40010
    WXBizMsgCrypt_GenReturnXml_Error = -40011


class WeWorkError(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __repr__(self):
        return f"WeWorkError(errcode={self.errcode},errmsg={self.errmsg})"

    def __str__(self):
        return self.__repr__()
