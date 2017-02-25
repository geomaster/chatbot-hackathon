
print('test')
from bot.console import console_loop
from bot.logic import handle
from bot.user_state import MockUserState
from bot.wit import wit


console_loop(handle)

    