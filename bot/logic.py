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

def build_carousel_msg(phones, brand):
    attachment = dict()
    attachment['type'] = 'template'
    payload = dict()
    payload['template_type'] = 'generic'

    elements = []
    for phone in phones[brand]:
        phone_dict = dict()
        phone_dict['title'] = brand + ' ' + phone['model']
        phone_dict['image_url'] = phone['img']
        phone_dict['subtitle'] = 'Telenor Ponuda'
        action = dict()
        action['type'] = 'web_url'
        action['url'] = phone['link']
        phone_dict['default_action'] = action

        elements.append(phone_dict)

    payload['elements'] = elements
    attachment['payload'] = payload
    message = dict()
    message['attachment'] = attachment
    return message



def load_content():
    content_file_loc = 'bot/content.json'
    with open(content_file_loc, encoding='utf-8') as content_file:
        content_json = json.load(content_file)
    phones = content_json['phones']
    return phones

INIT_QUIZ = {'text': 'KViiiz'}

def handle(user_id, msg, timestamp, send_fn):
    if msg == "Reset":
        create_user(user_id)
        return
    if msg == "Survey":
        send_fn(INIT_QUIZ)
        generate_survey(user_id)
        set_is_active_survey(user_id, True)
        set_survey_step(user_id, 0)
        send_fn(get_survey_question_at(user_id, 0)['message_json'])
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
            question = get_survey_question_at(user_id, step)
            add_survey_question_answer(question['question_id'], msg) # TODO: payload
            step += 1
            set_survey_step(user_id, step)
            if step == get_survey_length(user_id):
                # survey over
                send_fn(THANKS)
                set_is_active_survey(user_id, False)
                # set_last_survey_timestamp(user_id, timestamp)
            else:
                send_fn(get_survey_question_at(user_id, step)['message_json'])
        else:
            # answer questions
            intent = get_intent(msg)
            if intent == 'devices':
                for brand in phones:
                    if brand in msg:
                        carousel = build_carousel_msg(phones, brand)
                        send_fn({'text':'Ponuda telefona!'})
                        send_fn(carousel)
                        return
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

phones = load_content()
