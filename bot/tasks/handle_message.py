from ..celery import celery_app as app

@app.task
def handle_message(body):
    print("Handling message {0}".format(body))
