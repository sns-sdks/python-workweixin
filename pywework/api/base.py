"""
    Api 抽象
"""

import requests

from pywework.error import WeWorkError


class BaseApi:
    BASE_URL = 'https://qyapi.weixin.qq.com'

    def __init__(self):
        self._session = requests.Session()
        self.access_token = None

    def get_access_token(self):
        raise NotImplementedError

    def refresh_access_token(self):
        raise NotImplementedError

    def _request(self, url, method='GET', data=None, json=None, enforce_auth=True):
        if data is None:
            data = {}

        if method == 'POST':
            resp = 1
        elif method == 'GET':
            resp = self._session.get(url=url, params=data)
        else:
            resp = 0
        return resp

    @staticmethod
    def _check_response(resp_data):
        errcode = resp_data.get('errcode')
        errmsg = resp_data.get('errmsg')
        if errcode == 0:
            return resp_data
        else:
            raise WeWorkError(errcode, errmsg)

    @staticmethod
    def _token_expired(errcode):
        # Refer: https://work.weixin.qq.com/api/doc#90000/90139/90313
        if errcode in [42001, 40014]:
            return True
        return False
