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

def receive_message():
    messages_ref = db.child("message")

    def message_callback(message):
        global latest_msg, messages

        result = message.val()
        if result:
            brutha = list(result['messages'].items())
            last_key, main_val = brutha[-1]
            db_color = main_val['color'] if main_val['color'] and 7 >= main_val['color'] >= 0 else 3

            if last_key != latest_msg:
                oklahoma = ((main_val['username'],main_val['message']), db_color)
                messages.append(oklahoma)
                latest_msg = last_key
            else:
                return

    while True:
        new_message = messages_ref.get()
        if new_message:
            message_callback(new_message)


if __name__ == "__main__":
    receive_message()
