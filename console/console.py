import json
import uuid
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from pygments import highlight, lexers, formatters

def send_callback(response):
    ret = { "text": response["text"].decode("utf-8") }
    if response.get("quickreplies"):
        ret["quickreplies"] = response["quickreplies"]

    resp_json = json.dumps(ret, indent=2, ensure_ascii=False)
    colorful_json = highlight(resp_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)

def console_loop(handle_via_wit):
    uid = uuid.uuid1()
    history = InMemoryHistory()
    while True:
        q = prompt("> ", history=history).rstrip()
        if q == "quit":
            break
        handle_via_wit(uid, q, None, send_callback)
