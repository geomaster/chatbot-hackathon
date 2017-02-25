import redis
import json
import time

r = redis.StrictRedis()

# SETUP
USER_DATA = "users"
USER_QUESTION_DATA = "user_questions"
SURVEY_QUESTION_DATA = "survey_questions"

if r.get("next_user_id") is None:
    r.set("next_user_id", 0)
if r.get("next_user_question_id") is None:
    r.set("next_user_question_id", 0)
if r.get("next_survey_question_id") is None:
    r.set("next_survey_question_id", 0)


# SURVEY STUFF


def get_next_survey_question_id():
    next_id = int(r.get("next_survey_question_id"))
    r.incr("next_survey_question_id")
    return next_id


def add_survey_question(quick_replies_list, message_json_string, bucket):
    next_id = get_next_survey_question_id()
    quick_replies_dict = dict((reply, 0) for reply in quick_replies_list)
    message_dict = json.loads(message_json_string)

    survey_question_dict = {
        "survey_question_id": next_id,
        "quick_replies": quick_replies_dict,
        "message_json": message_dict,
        "bucket": bucket
    }

    survey_question_string = json.dumps(survey_question_dict)

    r.hmset(SURVEY_QUESTION_DATA, {next_id: survey_question_string})


def get_survey_question(s_question_id):
    s_question_dict = json.loads(r.hmget(SURVEY_QUESTION_DATA, s_question_id).decode("utf-8"))
    return s_question_dict


def set_survey_question(s_question_id, s_question_dict):
    r.hmset(SURVEY_QUESTION_DATA, {s_question_id: json.dump(s_question_dict)})


def add_survey_question_answer(s_question_id, answer):
    s_question = get_survey_question(s_question_id)
    s_question["quick_replies"][answer] += 1
    set_survey_question(s_question_id, s_question)

# USER STUFF


# Simulates auto-increment
def get_next_user_id():
    next_id = int(r.get("next_user_id"))
    r.incr("next_user_id")
    return next_id


def get_user_dict(user_id):
    user_dict = json.loads(r.hget(USER_DATA, user_id).decode('utf-8'))
    return user_dict


def set_user_dict(user_id, user_dict):
    r.hmset(USER_DATA, {user_id: json.dumps(user_dict)})


def get_user_status(user_id):
    user_dict = get_user_dict(user_id)
    return user_dict["new_user"]


def set_user_status(user_id, value):
    user_dict = get_user_dict(user_id)
    user_dict["new_user"] = value
    set_user_dict(user_id, user_dict)


def is_created(user_id):
    if r.hmget(USER_DATA, user_id)[0] is None:
        return False
    return True


def create_user(user_id):
    user = dict()
    # user_id = get_next_user_id()
    user["user_id"] = user_id
    user["new_user"] = 0  # 0 is false, 1 is true, 2 is awaiting for opt in
    user["opted_in"] = False
    user["is_active_survey"] = False
    user["survey_questions"] = []
    user["survey_step"] = -1
    user["last_survey_timestamp"] = 0

    user_string = json.dumps(user)

    r.hmset(USER_DATA, {user_id: user_string})
    # to decode:
    # json.loads(r.hget(USER_DATA, USER_ID).decode('utf-8'))


def is_active_survey(user_id):
    user_dict = get_user_dict(user_id)
    return user_dict["is_active_survey"]


def set_is_active_survey(user_id, value):
    user_dict = get_user_dict(user_id)
    user_dict["is_active_survey"] = value
    set_user_dict(user_id, user_dict)


def get_opted_in(user_id):
    user_dict = get_user_dict(user_id)
    print("Get ", user_dict["opted_in"])
    return user_dict["opted_in"]


def set_opted_in(user_id, value):
    print("Set ", value)
    user_dict = get_user_dict(user_id)
    user_dict["opted_in"] = value
    set_user_dict(user_id, user_dict)


def get_survey_step(user_id):
    user_dict = get_user_dict(user_id)
    return user_dict["survey_step"]


def set_survey_step(user_id, value):
    user_dict = get_user_dict(user_id)
    user_dict["survey_step"] = value
    set_user_dict(user_id, user_dict)


def set_last_survey_timestamp(user_id, timestamp):
    user_dict = get_user_dict(user_id)
    user_dict["last_survey_timestamp"] = timestamp
    set_user_dict(user_id, user_dict)

def generate_survey():
    # TODO
    return None


def get_users_to_survey():
    now = time.time()

    all_users = r.hgetall(USER_DATA)

    raise NotImplementedError("implement dis")


def get_survey(user_id):
    user_dict = get_user_dict(user_id)
    survey_question_ids = user_dict["survey_questions"]
    res = [get_survey_question(s_question_id) for s_question_id in survey_question_ids]
    res = [d["message_json"]["text"] for d in res]
    return res


def get_survey_question_at(user_id, step):
    user_dict = get_user_dict(user_id)
    s_q_id = user_dict["survey_questions"][step]
    return get_survey_question(s_q_id)


def get_survey_length(user_id):
    user_dict = get_user_dict(user_id)
    return len(user_dict["survey_questions"])


# USER QUESTIONS


def get_next_question_id():
    next_id = int(r.get("next_question_id"))
    r.incr("next_question_id")
    return next_id


def add_user_question(user_id, text, bucket):
    question = dict()
    question_id = get_next_question_id()

    question["question_id"] = question_id
    question["user_id"] = user_id
    question["bucket"] = bucket

    question_string = json.dumps(question)
    r.hmset(USER_QUESTION_DATA, {user_id: question_string})  # THESE ARE MAPPED BY USER_ID


# TODO:
# database.get_users_to_survey(curr_time - SURVEY_DELAY)
# database.generate_survey(user_id)

# DONE:
# database.is_active_survey(user_id)
# database.get_opted_in(uid)
# database.set_opted_in(user_id, False)
# database.set_is_active_survey(user_id, False)
# database.get_user_status(user_id)
# database.set_user_status(user_id, 1)
# database.add_user_question(user_id, msg, bucket)
# database.get_survey_step(user_id)
# database.set_survey_step(step)
# database.add_survey_question(q_reply_list, msg_json, bucket)
# database.set_last_survey_timestamp(user_id, timestamp)
# database.get_survey_question(s_question_id)
# database.get_survey(user_id)
# database.get_survey_question_at(user_id, step)
# database.add_survey_question_answer(curr_q_id, msg)


# user:
#     ..
# user_questions:
#     skup questiona
#     svaki question:
#         question_id
#         user_id
#         text
#         bucket
#
# survey_questions:
#     skup questiona
#     svaki question:
#         question_id
#         dict: string(quickrep) -> ppl_answered
#         message json
#         bucket (string)
