"""
    Api 抽象
"""

import logging

import requests

from pywework.error import ErrorCode, WeWorkError

logger = logging.getLogger(__name__)


class BaseApi:
    BASE_URL = 'https://qyapi.weixin.qq.com'
    DEFAULT_TIMEOUT = 1
    DEFAULT_RETRIES = 3

    def __init__(self):
        self._session = requests.Session()
        self.access_token = None

    def get_access_token(self):
        raise NotImplementedError

    def refresh_access_token(self):
        raise NotImplementedError

    def _request(self, url, method='GET', params=None, data=None, enforce_auth=True, retries=DEFAULT_RETRIES):
        if params is None:
            params = {}
        if data is not None:
            method = 'POST'
        logging.debug(f"Send request {self.DEFAULT_RETRIES - retries + 1} times")
        # 默认请求均主动添加 token
        if enforce_auth:
            if data is not None and "access_token" not in data:
                data['access_token'] = self.access_token
                params['access_token'] = self.access_token
            elif "access_token" not in params:
                params['access_token'] = self.access_token

        if method == 'POST':
            logging.debug(f"POST to {url}, json is {data}.")
            resp = self._session.post(url=url, params=params, json=data)
        elif method == 'GET':
            resp = self._session.get(url=url, params=params)
        else:
            raise WeWorkError(ErrorCode.NOT_SUPPORT_METHOD, f"Not support method for {method}.")

        resp_data = resp.json()
        if self._token_expired(resp_data.get('errcode')):
            self.refresh_access_token()
            # 执行重试
            self._request(url, method, params, data, enforce_auth, retries - 1)

        return self._check_response(resp_data)

    @staticmethod
    def _check_response(resp_data):
        errcode = resp_data.get('errcode')
        errmsg = resp_data.get('errmsg')
        if errcode == 0:
            return resp_data
        else:
            logging.debug(f'Origin response is: {resp_data}.')
            raise WeWorkError(errcode, errmsg)

    @staticmethod
    def _token_expired(errcode):
        # Refer: https://work.weixin.qq.com/api/doc#90000/90139/90313
        if errcode in [42001, 40014]:
            return True
        return False
