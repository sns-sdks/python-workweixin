""" error """


class WeWorkError(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __repr__(self):
        return f"WeWorkError(errcode={self.errcode},errmsg={self.errmsg})"

    def __str__(self):
        return self.__repr__()
