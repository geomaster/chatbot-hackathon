from ..celery import celery_app as app
from . import send_message
from ..logic import handle
from .send_message import send_message
from ..rediss import redis
from ..user_state import RedisUserState
from ..wit import wit
from .import *
from ..database import *
from ..logic import *
import time

SURVEY_DELAY = 60

@app.task(ignore_result=True)
def init_survey():
    user_ids = get_users_to_survey()
    for user_id in user_ids:
        if get_opted_in(user_id):
            generate_survey(user_id)
            set_is_active_survey(user_id, True)
            set_survey_step(0)
            send_message(get_survey_question(user_id)['message_json'])

'''
user: 
    new_user: True/False (True)
    opted_in: True/False (None)
    is_active_survey: True/False (False)
    survey_step: Int (-1)
    survey: json lista surveyQuestions (None)

questions:



'''