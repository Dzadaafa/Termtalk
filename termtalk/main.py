import curses
import pyrebase
import os
from colorama import Fore, Style
import json
import threading
import random
import receiver as rcvr

# Firebase configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
flag_file = os.path.join(script_dir, 'exit_flag')
config_file = os.path.join(script_dir, 'config.json')

with open(config_file, 'r') as f:
    config = json.load(f)

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

colors = [
    curses.COLOR_BLACK, curses.COLOR_WHITE,
    curses.COLOR_CYAN, curses.COLOR_GREEN,
    curses.COLOR_MAGENTA, curses.COLOR_RED,
    curses.COLOR_BLUE, curses.COLOR_YELLOW
]

username:str
color:int


def main(stdscr):
    global inputUsr, username, colors

    curses.start_color()
    if not curses.has_colors():
        stdscr.addstr(0, 0, "Your terminal does not support colors.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()

    for i, colored in enumerate(colors):
        if 2 <= i <= 7:
            curses.init_pair(i + 1, colored, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()

    # Get the screen height and width
    height, width = stdscr.getmaxyx()

    # List to store the printed numbers
    lines = []
    inputUsr = ""

    while True:
        messages = rcvr.messages
        # Check if we have new messages
        while len(messages) > 0:
            new_message = messages.pop(0)
            
            # Check if we have reached the height limit for numbers
            if len(lines) >= height - 2:
                # Remove the oldest number from the top
                lines.pop(0)
            
            # Add the new message to the list
            lines.append(new_message)

        # Clear the screen
        stdscr.clear()

        stdscr.addstr(0, int((width / 2) - len(username)), f"Termtalk", curses.color_pair(4) | curses.A_UNDERLINE )

        for idx, line in enumerate(lines):
            msg, usncolor = line
            usn, usnmsg = msg
            stdscr.addstr(idx + 2, 0, f"{usn}: ", curses.color_pair(usncolor + 1))
            stdscr.addstr(usnmsg)

        # Print the input prompt at the bottom
        stdscr.addstr(height - 4, 0, "-" * width)
        stdscr.addstr(height - 3, 0, "(Esc) Exit", curses.A_DIM)
        stdscr.addstr(height - 2, 0, "-" * width)
        stdscr.addstr(height - 1, 0, f"{username}: ", curses.color_pair(color + 1))
        stdscr.addstr(str(inputUsr))

        # Refresh the screen to see the changes
        stdscr.refresh()

        # Get user input (non-blocking)
        stdscr.timeout(10)
        key = stdscr.getch()

        # If the user presses 'ESC', break the loop
        if key == 27:
            break
        elif key == 8 or key == 127:  # Backspace
            inputUsr = inputUsr[:-1]
        elif key == 10:  # Enter
            try:
                messages_ref = db.child("messages")

                messages_ref.push({
                    "username": username,
                    "message": inputUsr,
                    "color": color
                })
                inputUsr = ""
            except Exception as e:
                pass
        else:
            if 32 <= key <= 126 and len(inputUsr) <= 40:
                inputUsr = inputUsr + chr(key)

def start():
    global username, color
    username = input(f"{Fore.GREEN}Enter your username:{Style.RESET_ALL} ")
    color = random.randint(2, 7)
    # Run the message receiving function in a separate thread
    receive_thread = threading.Thread(target=rcvr.receive_message, daemon=True)
    receive_thread.start()

    # Initialize curses
    curses.wrapper(main)

if __name__ == "__main__":
    start()