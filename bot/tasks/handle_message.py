from ..celery import celery_app as app
from . import send_message
from ..logic import handle
from .send_message import send_message
from ..rediss import redis
from ..user_state import RedisUserState
from ..wit import wit
import time

@app.task(ignore_result=True)
def handle_message(sender_id, msg, timestamp):
    # user_state = RedisUserState(sender_id, redis)

    def send_fn(message):
        send_message.delay(sender_id, message)

    '''if not msg["text"].startswith("`"):
        meaning = wit.message(msg["text"])
    else:
        # Don't spam Wit with debug commands
        meaning = { "_text": msg["text"] }'''

    handle(sender_id, msg["text"], timestamp, send_fn)
    # user_state.set_state_id(new_state_id)
