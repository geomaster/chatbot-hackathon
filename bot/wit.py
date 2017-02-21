from __future__ import absolute_import
from wit import Wit
from .secrets import WIT_TOKEN
from .tasks.send_message import send_text_message

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def del_if_exists(ctx, key):
    if key in ctx.keys():
        del ctx[key]

def send(request, response):
    recipient_id = request["session_id"]
    text = response["text"].decode("utf-8")
    send_text_message.delay(recipient_id, text)

def get_packages(request):
    ctx = request["context"]
    entities = request["entities"]
    typ = first_entity_value(entities, "package_type")
    if typ:
        ctx["packages"] = "{0} LUDILO, {0} SIMPA, {0} BIZNIS".format(typ)
        del_if_exists(ctx, "missing_package_type")
    else:
        ctx["missing_package_type"] = True
        del_if_exists(ctx, "package_type")

    return ctx

def get_phones(request):
    ctx = request["context"]
    entities = request["entities"]
    brand = first_entity_value(entities, "brand")
    if brand:
        ctx["phones"] = "{0} BEJZIK 210 16GB, {0} 555333 UBER NATIONALIST 32GB, {0} XPS GRAND 420+ 64GB".format(brand)
        del_if_exists(ctx, "brand_missing")
    else:
        ctx["brand_missing"] = True
        del_if_exists(ctx, "phones")

    return ctx

def handle_via_wit(sender_id, text):
    wit.run_actions(session_id=sender_id, message=text)

actions = {
    'send': send,
    'get_phones': get_phones,
    'get_packages': get_packages
}

wit = Wit(access_token=WIT_TOKEN, actions=actions)

