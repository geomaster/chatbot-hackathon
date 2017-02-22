from ..celery import celery_app as app
from ..wit import handle_via_wit
from . import send_message
import time

@app.task(ignore_result=True)
def handle_message(sender_id, msg):
    print("[{0}] Handling message at {1}".format(msg["mid"], time.time()))
    handle_via_wit(sender_id, msg.get("text"), send_message)
