"""
    XML 格式的消息
"""
import xml.etree.cElementTree as eT

from pywework.error import WeWorkError, ErrorCode
from . import msg_struct


class DefaultDict(dict):
    """ 默认空 value 字典 """

    def __missing__(self, key):
        return ""


class XMLMessage:
    SUPPORT_BUILD_TYPE = {
        "respond": msg_struct.XML_RESPOND_STRUCT,
        "text": msg_struct.XML_TEXT_STRUCT,
        "media": msg_struct.XML_MEDIA_STRUCT,
        "link": msg_struct.XML_LINK_STRUCT,
        "voice": msg_struct.XML_VOICE_STRUCT,
        "video": msg_struct.XML_VIDEO_STRUCT,
        "location": msg_struct.XML_LOCATION_STRUCT,
    }
    SUPPORT_PARSE_TYPE = {
        "respond": msg_struct.XML_RESPOND_KEY,
        "text": msg_struct.XML_TEXT_KEY,
        "media": msg_struct.XML_MEDIA_KEY,
        "link": msg_struct.XML_LINK_KEY,
        "voice": msg_struct.XML_VOICE_KEY,
        "video": msg_struct.XML_VIDEO_KEY,
        "location": msg_struct.XML_LOCATION_KEY,
    }

    def build_message(self, msg_type: str, **kwargs) -> str:
        if msg_type not in self.SUPPORT_BUILD_TYPE:
            raise WeWorkError(
                ErrorCode.NOT_SUPPORT_TYPE,
                f"Message type for {msg_type} not support to build.",
            )
        base_info = self.SUPPORT_BUILD_TYPE[msg_type]
        return base_info.format_map(DefaultDict(kwargs))

    def parse_message(self, message: str, respond: bool = False) -> dict:
        """
        从 XML 字符串中解析出各个字段
        :param message: XML 字符串
        :param respond: 如果是上层响应消息体 需要指定为 True
        :return:
        """
        xml_tree = eT.fromstring(message)
        if respond:
            msg_type = "respond"
        else:
            msg_type = xml_tree.find("MsgType").text
        if msg_type not in self.SUPPORT_PARSE_TYPE:
            raise WeWorkError(
                ErrorCode.NOT_SUPPORT_TYPE,
                f"Message type for {msg_type} not support to parse.",
            )
        res = {}
        for key in self.SUPPORT_PARSE_TYPE[msg_type]:
            res[key] = xml_tree.find(key).text
        return res


xml_message = XMLMessage()
