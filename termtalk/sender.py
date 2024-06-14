import pyrebase
import json
import random
import string
import os
from colorama import Fore, Style, init

#colorama things
resetStyle = Style.RESET_ALL
init()

# Initialize the Firebase app
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'config.json')
flag_file = os.path.join(script_dir, 'exit_flag')

with open(config_file, 'r') as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def user_input():
    username = input(f"{Fore.GREEN}Enter your username:{resetStyle} ")
    print("=" * 50)
    print("Welcome, "+f"{Fore.GREEN}{username}{resetStyle}! You can start typing your messages.")

    
    while True:
        user_text = input(f"Enter your message {Fore.RED}('exit' to quit){resetStyle}: ")
        if user_text.lower() == 'exit':
            print(f"{Fore.RED}Exiting...")
            # Create an empty flag file to signal the receiver to exit
            open(flag_file, 'a').close()
            break

        # Push the message to Firebase
        try:
            messages_ref = db.child("messages")

            messages_ref.push({
                "username": username,
                "message": user_text
            })
        except Exception as e:
            print(f"Error sending message: {e}")


def unique_key(length=20):
    characters = string.ascii_letters + string.digits + '-_'
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    user_input()
