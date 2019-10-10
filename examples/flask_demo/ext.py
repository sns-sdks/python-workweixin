from pywework.api.work import Api

# WeWork
CORP_ID = 'xx'
CORP_SECRET = 'xx'
AGENT_ID = 'xx'

R_TOKEN = 'xx'
R_AES_KEY = 'xx'

wework = Api(
    corp_id=CORP_ID, corp_secret=CORP_SECRET,
    agent_id=AGENT_ID,
    r_token=R_TOKEN, r_aes_key=R_AES_KEY
)
