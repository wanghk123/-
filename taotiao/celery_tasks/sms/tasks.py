
import json
from ronglian_sms_sdk import SmsSDK
from celery_tasks.main import celery_app

accId = '8a216da8802d68fe01804495fcc80493'
accToken = 'a0e37fdd5a044665b583eae19f757f1b'
appId = '8a216da8802d68fe01804495fdc6049a'


@celery_app.task(name='send_message')
def send_message(mobile, code, time):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    datas = (code, time // 60)
    resp = sdk.sendMessage(tid, mobile, datas)
    status_code = json.loads(resp).get('statusCode')
    return True if status_code == '000000' else False

# 15670355589