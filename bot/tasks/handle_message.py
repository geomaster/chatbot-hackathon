from ..celery import celery_app as app
from . import send_message
from ..logic import handle
from .send_message import send_message
from ..redis import redis
from ..user_state import RedisUserState
from ..wit import wit
import time

@app.task(ignore_result=True)
def handle_message(sender_id, msg):
    user_state = RedisUserState(sender_id, redis)

    if msg.get("text") == "`state?":
        send_message.delay(sender_id, { "text": user_state.get_state_id() or "None" })
        return
    elif msg.get("text").startswith("`state="):
        new_state = msg.get("text")[7:]
        user_state.set_state_id(new_state)
        send_message.delay(sender_id, { "text": "Set {0}".format(new_state) })
        return

    def send_fn(message):
        send_message.delay(sender_id, message)

    meaning = wit.message(msg["text"])
    new_state = handle(user_state, meaning, send_fn)
    user_state.set_state_id(new_state)
