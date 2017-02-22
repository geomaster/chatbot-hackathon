import json
import uuid
from pygments import highlight, lexers, formatters
from termcolor import colored
from sys import stdout

def send_callback(msg):
    resp_json = json.dumps(msg, indent=2, ensure_ascii=False)
    colorful_json = highlight(resp_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)

def console_loop(handle, wit, user_state):
    while True:
        state_id = user_state.get_state_id() or "none"
        stdout.write("[{0}]".format(colored(state_id, 'cyan')))
        q = input("> ").rstrip()

        if q == "quit":
            break

        try:
            meaning = wit.message(q)
            new_state_id = handle(user_state, meaning, send_callback)
            user_state.set_state_id(new_state_id)
        except Exception:
            print(colored("Error contacting Wit.", "red"))
