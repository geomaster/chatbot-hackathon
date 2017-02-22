import json
import uuid
import traceback
from pygments import highlight, lexers, formatters
from termcolor import colored
from sys import stdout

def print_json(json_msg):
    resp_json = json.dumps(json_msg, indent=2, ensure_ascii=False)
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
            print("==Wit response:")
            meaning = wit.message(q)
            print_json(meaning)
            print("==Bot message:")
            new_state_id = handle(user_state, meaning, print_json)
            user_state.set_state_id(new_state_id)
        except Exception as e:
            print(colored("Error while responding: ", "red"), traceback.print_exc())
