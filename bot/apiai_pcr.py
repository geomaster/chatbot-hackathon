import apiai
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

CLIENT_ACCESS_TOKEN = '0882a9ceebf04bf28d7cd4cf95c0f083'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def get_intent(text):
    r = ai.text_request()
    r.session_id = 'OGI_ID'

    r.query = text

    res = json.loads(r.getresponse().read())

    if res['result'] and res['result']['metadata'] and res['result']['metadata']['intentName']:
        return res['result']['metadata']['intentName']
    else:
        return None