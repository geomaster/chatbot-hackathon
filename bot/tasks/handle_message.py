from ..celery import celery_app as app
from send_message import send_text_message

@app.task
def handle_message(body):
    print("Handling message {0}".format(body))
    send_text_message.delay("Alo, 555-333?")
