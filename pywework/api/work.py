"""
    消息推送
"""
import logging
import pathlib
import pickle

from .base import BaseApi
from pywework.error import ErrorCode, WeWorkError
from pywework.utils.param_checker import incompatible_validator

logger = logging.getLogger(__name__)


class Api(BaseApi):
    SUPPORT_TYPES = [
        "text",
        "image",
        "voice",
        "video",
        "file",
        "textcard",
        "news",
        "mpnews",
        "markdown",
        "miniprogram_notice",
        "taskcard",
    ]
    DEFAULT_TOKEN_FILE = "message_token.pickle"

    def __init__(self, corp_id, corp_secret, agent_id, token_file=None):
        super().__init__()
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.agent_id = agent_id
        self.token_file = token_file
        self.initial()

    def initial(self):
        if self.token_file is None:
            self.token_file = self.DEFAULT_TOKEN_FILE
        token_path = pathlib.Path(self.token_file)
        if token_path.exists():
            with token_path.open("rb") as f:
                token_info = pickle.load(f)
            self.access_token = token_info["access_token"]
        else:
            self.get_access_token()

    def get_access_token(self):
        if self.access_token is None:
            self.refresh_access_token()
        return self.access_token

    def refresh_access_token(self):
        params = {"corpid": self.corp_id, "corpsecret": self.corp_secret}
        resp = self._request(
            self.BASE_URL + "/cgi-bin/gettoken", params=params, enforce_auth=False
        )
        self.access_token = resp.get("access_token")

        # write to pickle
        token_path = pathlib.Path(self.token_file)
        with token_path.open("ab") as f:
            pickle.dump(resp, f)

    def send_text(
        self, text, to_user=None, to_party=None, to_tag=None, safe=0, enable_id_trans=0
    ):
        incompatible_validator(to_user=to_user, to_party=to_party, to_tag=to_tag)
        if text is None:
            raise WeWorkError(ErrorCode.MISSION_PARAM, f"Need provide text info")
        text_info = {"content": text}
        return self._send(
            "text",
            text_info,
            to_user=to_user,
            to_party=to_party,
            to_tag=to_tag,
            safe=safe,
            enable_id_trans=enable_id_trans,
        )

    def send_textcard(
        self,
        to_user=None,
        to_party=None,
        to_tag=None,
        title=None,
        description=None,
        url=None,
        btn_text=None,
        enable_id_trans=0,
    ):

        incompatible_validator(to_user=to_user, to_party=to_party, to_tag=to_tag)
        text_card = {
            "title": title,
            "description": description,
            "url": url,
            "btntxt": btn_text,
        }
        return self._send(
            "textcard",
            text_card,
            to_user=to_user,
            to_party=to_party,
            to_tag=to_tag,
            enable_id_trans=enable_id_trans,
        )

    def send_markdown(self, markdown, to_user=None, to_party=None, to_tag=None):
        incompatible_validator(to_user=to_user, to_party=to_party, to_tag=to_tag)
        markdown_info = {"content": markdown}

        return self._send(
            "markdown", markdown_info, to_user=to_user, to_party=to_party, to_tag=to_tag
        )

    def _send(self, msg_type, info, to_user=None, to_party=None, to_tag=None, **kwargs):
        if msg_type not in self.SUPPORT_TYPES:
            raise WeWorkError(ErrorCode.NOT_SUPPORT_TYPE, "message type not support")

        data = {
            "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
            "msgtype": msg_type,
            "agentid": self.agent_id,
            msg_type: info,
        }
        if kwargs:
            data.update(kwargs)

        resp = self._request(self.BASE_URL + "/cgi-bin/message/send", data=data)

        return resp
