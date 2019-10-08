""" error """


class ErrorCode:
    NOT_SUPPORT_METHOD = 11001
    NOT_SUPPORT_TYPE = 11002
    INVALID_PARAM = 11003
    MISSION_PARAM = 11004


class WeWorkError(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __repr__(self):
        return f"WeWorkError(errcode={self.errcode},errmsg={self.errmsg})"

    def __str__(self):
        return self.__repr__()
