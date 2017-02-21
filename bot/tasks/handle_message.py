from ..celery import celery_app as app
from .send_message import send_text_message

@app.task
def handle_message(sender_id, body):
    print("Handling message {0}".format(body))
    send_text_message.delay(sender_id, "Alo, 555-333?")
