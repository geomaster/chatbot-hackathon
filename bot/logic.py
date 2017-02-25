from .graph import Graph
from .import *
from .apiai_pcr import get_intent
from .forum import search
from .database import *

'''
def get_wit_info(meaning):
    """Extract valuable information from a Wit meaning object."""
    wit_info = dict()
    for entity, val_list in meaning['entities'].items():
        for val in val_list:
            if val.get('suggested') != True:
                if not entity in wit_info:
                    wit_info[entity] = []
                wit_info[entity].append(val['value'])
    print(wit_info)  # debug
    return wit_info

def handle_debug_command(node, msg):
    if msg == '`state?':
        return (node, node or 'None')
    elif msg.startswith('`state='):
        new_node = msg[7:]
        return (new_node, 'Set {0}'.format(new_node))
    return None
'''

THANKS = {'text': 'Hvala na anketi :)'}
NO_ANS = {'text': 'Nemamo odgovor'}
INTRO_MSG = {
                "text": "Ja sam Telenor bot, hoces da ti saljem spam?",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Da!",
                        "payload": "empty"
                    },
                    {
                        "content_type": "text",
                        "title": "Ne :(",
                        "payload": "empty"
                    }
                ]
            }
OPTED_IN = {'text': 'Hvala!'}
NO_OPTED_IN = {'text': 'Steta!'}
SATISFACTION = {
                "text": "Da li ste zadovoljni?",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Da!",
                        "payload": "empty"
                    },
                    {
                        "content_type": "text",
                        "title": "Ne :(",
                        "payload": "empty"
                    }
                ]
            }

def handle(user_id, msg, timestamp, send_fn):
    if msg == "Reset":
        create_user(user_id)
        return
    if not is_created(user_id):
        create_user(user_id)
    if get_user_status(user_id) == 0:
        set_user_status(user_id, 1)
        send_fn(INTRO_MSG)
    elif get_user_status(user_id) == 1:
        set_user_status(user_id, 2)
        intent = get_intent(msg)
        if intent:
            opted_in = intent
        else:
            opted_in = "no"
        if opted_in == "yes":
            set_opted_in(user_id, True)
            send_fn(OPTED_IN)
        else:
            set_opted_in(user_id, False)
            send_fn(NO_OPTED_IN)
    else:
        if is_active_survey(user_id):
            # survey = get_survey(user_id)
            step = get_survey_step(user_id)
            curr_q_id = get_survey_question_at(user_id, step)
            add_survey_question_answer(curr_q_id, msg) # TODO: payload
            step += 1
            set_survey_step(user_id, step)
            if step == get_survey_length(user_id):
                # survey over
                send_fn(THANKS)
                set_is_active_survey(user_id, False)
                # set_last_survey_timestamp(user_id, timestamp)
            else:
                next_q_id = get_survey_question_at(user_id, step)
                send_fn(get_survey_question(next_q_id))
        else:
            intent = get_intent(msg)
            if intent != 'unclassified':
                bucket = intent
            else:
                bucket = "Ostalo"
            ans = search(msg)
            if ans:
                send_fn({'text': 'Vas odgovor:\n\n' + ans.get('q') + "\n\n" + ans.get('a') + '\n\n' + bucket})
                # send_fn(SATISFACTION)
                satisfied = True
            else:
                send_fn(NO_ANS)
                satisfied = False
            add_user_question_to_question_data(user_id, msg, bucket, satisfied)

