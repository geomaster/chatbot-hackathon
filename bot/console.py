import json
import uuid
import traceback
from pygments import highlight, lexers, formatters
from termcolor import colored
from sys import stdout
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import time
from .database import *

USER_ID = -1

def print_json(json_msg):
    resp_json = json.dumps(json_msg, indent=2, ensure_ascii=False)
    colorful_json = highlight(resp_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)

def console_loop(handle):
    history = InMemoryHistory()
    while True:
        if is_created(USER_ID):
            state_id = str(get_user_status(USER_ID)) + ":" + str(get_opted_in(USER_ID)) + ":" + str(is_active_survey(USER_ID))
        else:
            state_id = "/"
        stdout.write("[{0}]".format(colored(state_id, 'cyan')))
        q = prompt("> ", history=history).rstrip()
        curr_time = time.time()
        if q == "quit":
            break
        try:
            handle(USER_ID, q, curr_time, print_json)
        except Exception as e:
            print(colored("Error while responding: ", "red"), traceback.print_exc())
