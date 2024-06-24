import pyrebase
import os
import platform
from colorama import Fore, Style
import json
import random

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

def receive_message():
    messages_ref = db.child("message")

    def message_callback(message):
        global latest_msg

        result = message.val()
        if result:
            messages = list(result['messages'].items())
            last_key, main_val = messages[-1]
            color = main_val['color']

            if last_key != latest_msg:
                print(f"{colors[color]}{main_val['username']}: {Fore.WHITE}{main_val['message']}")
                latest_msg = last_key
            else:
                return

    while True:
        if os.path.exists(flag_file):
            break
        else:
            new_message = messages_ref.get()
            if new_message:
                message_callback(new_message)

    if platform.system() == "Windows":
        os.system("taskkill /F /IM cmd.exe")
    elif platform.system() == "Darwin":  # macOS
        os.system(
            "osascript -e 'tell application \"Terminal\" to close first window' & exit")
    else:  # Unix-like (Linux)
        os.system("kill -9 $PPID")


if __name__ == "__main__":
    receive_message()
