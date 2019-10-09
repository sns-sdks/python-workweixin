# 普通消息体的 XML 格式
# Refer: https://work.weixin.qq.com/api/doc#90000/90135/90239

XML_BASE_KEY = [
    'ToUserName', 'FromUserName', 'CreateTime', 'MsgType', 'MsgId', 'AgentID'
]

XML_TEXT_KEY = XML_BASE_KEY + [
    'Content'
]
XML_TEXT_STRUCT = (
    "<xml>"
    "<ToUserName><![CDATA[{ToUserName}]]></ToUserName>"
    "<FromUserName><![CDATA[{FromUserName}]]></FromUserName>"
    "<CreateTime>{CreateTime}</CreateTime>"
    "<MsgType><![CDATA[text]]></MsgType>"
    "<Content><![CDATA[{Content}]]></Content>"
    "<MsgId>{MsgId}</MsgId>"
    "<AgentID>{AgentID}</AgentID>"
    "</xml>"
)

XML_MEDIA_KEY = XML_BASE_KEY + [
    'PicUrl', 'MediaId'
]
XML_MEDIA_STRUCT = (
    "<xml>"
    "<ToUserName><![CDATA[{ToUserName}]]></ToUserName>"
    "<FromUserName><![CDATA[{FromUserName}]]></FromUserName>"
    "<CreateTime>{CreateTime}</CreateTime>"
    "<MsgType><![CDATA[image]]></MsgType>"
    "<PicUrl><![CDATA[{PicUrl}]]></PicUrl>"
    "<MediaId><![CDATA[{MediaId}]]></MediaId>"
    "<MsgId>{MsgId}</MsgId>"
    "<AgentID>{AgentID}</AgentID>"
    "</xml>"
)

XML_LINK_KEY = XML_BASE_KEY + [
    'Title', 'Description', 'PicUrl'
]
XML_LINK_STRUCT = (
    "<xml>"
    "<ToUserName><![CDATA[{ToUserName}]]></ToUserName>"
    "<FromUserName><![CDATA[{FromUserName}]]></FromUserName>"
    "<CreateTime>{CreateTime}</CreateTime>"
    "<MsgType><![CDATA[link]]></MsgType>"
    "<Title><![CDATA[{Title}]]></Title>"
    "<Description><![CDATA[{Description}]]></Description>"
    "<PicUrl><![CDATA[{PicUrl}]]></PicUrl>"
    "<MsgId>{MsgId}</MsgId>"
    "<AgentID>{AgentID}</AgentID>"
    "</xml>"
)

XML_VOICE_KEY = XML_BASE_KEY + [
    'MediaId', 'Format'
]
XML_VOICE_STRUCT = (
    "<xml>"
    "<ToUserName><![CDATA[{ToUserName}]]></ToUserName>"
    "<FromUserName><![CDATA[{FromUserName}]]></FromUserName>"
    "<CreateTime>{CreateTime}</CreateTime>"
    "<MsgType><![CDATA[voice]]></MsgType>"
    "<MediaId><![CDATA[{MediaId}]]></MediaId>"
    "<Format><![CDATA[{Format}]]></Format>"
    "<MsgId>{MsgId}</MsgId>"
    "<AgentID>{AgentID}</AgentID>"
    "</xml>"
)

XML_VIDEO_KEY = XML_BASE_KEY + [
    'MediaId', 'ThumbMediaId'
]
XML_VIDEO_STRUCT = (
    "<xml>"
    "<ToUserName><![CDATA[{ToUserName}]]></ToUserName>"
    "<FromUserName><![CDATA[{FromUserName}]]></FromUserName>"
    "<CreateTime>{CreateTime}</CreateTime>"
    "<MsgType><![CDATA[video]]></MsgType>"
    "<MediaId><![CDATA[{MediaId}]]></MediaId>"
    "<ThumbMediaId><![CDATA[{thumb_MediaId}]]></ThumbMediaId>"
    "<MsgId>{MsgId}</MsgId>"
    "<AgentID>{AgentID}</AgentID>"
    "</xml>"
)

XML_LOCATION_KEY = XML_BASE_KEY + [
    'Location_X', 'Location_Y', 'Scale', 'Label'
]
XML_LOCATION_STRUCT = (
    "<xml>"
    "<ToUserName><![CDATA[{ToUserName}]]></ToUserName>"
    "<FromUserName><![CDATA[{FromUserName}]]></FromUserName>"
    "<CreateTime>{CreateTime}</CreateTime>"
    "<MsgType><![CDATA[location]]></MsgType>"
    "<Location_X>{Location_X}</Location_X>"
    "<Location_Y>{Location_Y}</Location_Y>"
    "<Scale>{Scale}</Scale>"
    "<Label><![CDATA[{Label}]]></Label>"
    "<MsgId>{MsgId}</MsgId>"
    "<AgentID>{AgentID}</AgentID>"
    "<AppType><![CDATA[wxwork]]></AppType>"
    "</xml>"
)
