import pyrebase
import os
import platform
from colorama import Fore
import json

# import credential hehe
script_dir = os.path.dirname(os.path.abspath(__file__))
flag_file = os.path.join(script_dir, 'exit_flag')
config_file = os.path.join(script_dir, 'config.json')

with open(config_file, 'r') as f:
    config = json.load(f)

#colorama


firebase = pyrebase.initialize_app(config)
db = firebase.database()

colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, 
            Fore.BLUE, Fore.MAGENTA, Fore.CYAN, 
            Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, 
            Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, 
            Fore.LIGHTCYAN_EX]


latest_msg = ""
messages = []

def receive_message() -> list | None:
    messages_ref = db.child("message")

    def message_callback(message) -> list:
        global latest_msg, messages

        result = message.val()
        if result:
            listed_result = list(result['messages'].items())
            last_key, main_val = listed_result[-1]
            db_color = main_val['color'] if main_val['color'] and 7 >= main_val['color'] >= 0 else 3

            if last_key != latest_msg:
                final_result = ((main_val['username'],main_val['message']), db_color)
                messages.append(final_result)
                latest_msg = last_key
                return final_result
            else:
                return None

    while True:
        new_message = messages_ref.get()
        if new_message:
            message_callback(new_message)

def send_message(color:int, username:str, msg:str) -> bool:
    try:
        messages_ref = db.child("messages")

        messages_ref.push({
            "username": username,
            "message": msg,
            "color": color
        })

        return True
    except Exception as e:
        return False

