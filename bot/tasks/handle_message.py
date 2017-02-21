from ..celery import celery_app as app
from ..wit import handle_via_wit
from .send_message import send_text_message

@app.task
def handle_message(sender_id, msg):
    handle_via_wit(sender_id, msg.get("text"))
