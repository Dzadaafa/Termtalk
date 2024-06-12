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

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def is_single_message(data):
    # Check if the first value in the dictionary is a dictionary itself
    if isinstance(data, dict):
        first_value = next(iter(data.values()))
        return not isinstance(first_value, dict)
    return False


def receive_message():

    messages_ref = db.child("message").get()

    def message_callback(message):
        new_message = message.val()
        if new_message:
            print(new_message)

    while True:
        if os.path.exists(flag_file):
            break
        else:
            new_message = messages_ref.get()
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
