import redis
import json
import time

r = redis.StrictRedis()

# SETUP
SURVEY_MIN_DELTA_TIME = 30
SURVEY_QUESTIONS_COUNT = 3

USER_DATA = "users"
USER_QUESTION_DATA = "user_questions"
SURVEY_QUESTION_DATA = "survey_questions"


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
    user_data = dict()
    # user_id = get_next_user_id()
    user_data["user_id"] = user_id
    user_data["new_user"] = 0  # 0 is false, 1 is true, 2 is awaiting for opt in
    user_data["opted_in"] = False
    user_data["is_active_survey"] = False
    user_data["survey_questions"] = []
    user_data["survey_step"] = -1
    user_data["last_survey_timestamp"] = 0
    user_data["questions"] = []
    user_string = json.dumps(user_data)
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
    return user_dict["opted_in"]


def set_opted_in(user_id, value):
    user_dict = get_user_dict(user_id)
    user_dict["opted_in"] = value
    set_user_dict(user_id, user_dict)


def get_user_questions(user_id):
    user_dict = get_user_dict(user_id)
    return user_dict["questions"]


def add_user_question_to_user_data(user_id, u_question_id):
    user_dict = get_user_dict(user_id)
    user_dict["questions"].append(u_question_id)
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


def get_users_to_survey():
    now = time.time()
    ret = []

    all_users = r.hgetall(USER_DATA)
    for user, user_json in all_users.items():
        user_dict = json.loads(user_json.decode("utf-8"))
        if now - float(user_dict["last_survey_timestamp"]) > SURVEY_MIN_DELTA_TIME:
            ret.append(user_dict["user_id"])

    return ret


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


def generate_survey(user_id):
    user_dict = get_user_dict(user_id)

    ret = []
    counts = dict()
    for q_id in user_dict["questions"]:
        q_data = get_user_question_data(q_id)
        bucket = q_data["bucket"]
        if not bucket in counts:
            counts["bucket"] = 1
        else:
            counts["bucket"] += 1

    max_bucket = max(counts, key=counts.get)

    all_s_questions = json.loads(r.hgetall(SURVEY_QUESTION_DATA).decode('utf-8'))
    count_added = 0
    for s_q_id, s_q in all_s_questions:
        if s_q["bucket"] == max_bucket and count_added < SURVEY_QUESTIONS_COUNT:
            ret.append(s_q["message_json"]["text"])
            count_added += 1

    return ret


# USER QUESTIONS

def setup():
    r.flushall()

    if r.get("next_user_id") is None:
        r.set("next_user_id", 0)
    if r.get("next_user_question_id") is None:
        r.set("next_user_question_id", 0)
    if r.get("next_survey_question_id") is None:
        r.set("next_survey_question_id", 0)


def get_next_question_id():
    next_id = int(r.get("next_user_question_id"))
    r.incr("next_user_question_id")
    return next_id


def get_user_question_data(q_id):
    user_question_data = [q.decode('utf-8') for q in r.hmget(USER_QUESTION_DATA, q_id)]
    return user_question_data


def add_user_question_to_question_data(user_id, text, bucket, satisfied):
    question = dict()
    question_id = get_next_question_id()

    question["question_id"] = question_id
    question["text"] = text
    question["user_id"] = user_id
    question["bucket"] = bucket
    question["satisfied"] = satisfied

    question_string = json.dumps(question)

    r.hmset(USER_QUESTION_DATA, {question_id: question_string})
    add_user_question_to_user_data(user_id, question_id)


create_user(10)
add_user_question_to_question_data(10, "Ko te prati kuci?", "internet", True)
add_user_question_to_question_data(10, "Cao cao", "internet", True)


get_user_dict(10)
print(get_user_question_data(0))
print(get_user_question_data(1))
print(get_user_question_data(2))
