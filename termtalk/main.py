
import platform
import os
import time
import argparse
from . import sender, receiver
# import sender, receiver

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--destination", help="start the chat page individually", action="store_true")
parser.add_argument("-s", "--sender", help="start the chat sender individually", action="store_true")

arg = parser.parse_args()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
flag_file = os.path.join(script_dir, 'exit_flag')
receiver_path = os.path.join(script_dir, 'receiver.py')

def new_page_receiver():
    
    if platform.system() == "Windows":
        os.system(f'start cmd /k python {receiver_path}')
    elif platform.system() == "Darwin":  # macOS
        os.system(f'open -a Terminal python {receiver_path}')
    else:  # Assume Unix-like (Linux)
        os.system(f'gnome-terminal -- python3 {receiver_path}')


def start():
    if arg.destination:
        if os.path.exists(flag_file):
            os.remove(flag_file)
        receiver.receive_message()

    elif arg.sender:
        sender.user_input()

    else:
        if os.path.exists(flag_file):
            os.remove(flag_file)
        new_page_receiver()
        time.sleep(2)
        sender.user_input()

if __name__ == "__main__":
    start()


