from pywework.api.work import Api
from pywework.crypto.validation import MessageValidation
from pywework.message.xml import xml_message

# WeWork
CORP_ID = 'xx'
CORP_SECRET = 'xx'
AGENT_ID = 'xx'

R_TOKEN = 'xx'
R_AES_KEY = 'xx'

wework = Api(
    corp_id=CORP_ID, corp_secret=CORP_SECRET,
    agent_id=AGENT_ID
)

wework_msg_validation = MessageValidation(
    token=R_TOKEN, aes_key=R_AES_KEY, receive_id=CORP_ID
)

wework_msg_xml_parser = xml_message
