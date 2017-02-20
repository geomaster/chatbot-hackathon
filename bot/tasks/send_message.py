from ..celery import celery_app as app

@app.task
def send_message(body):
    print("Sending message {0}".format(body))
