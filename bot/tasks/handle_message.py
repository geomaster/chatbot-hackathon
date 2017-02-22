from ..celery import celery_app as app
from ..wit import handle_via_wit
from . import send_message
import time

@app.task(ignore_result=True)
def handle_message(sender_id, msg):
    send_message.send_text_message.delay(sender_id, "wit_bypass_test")
