from sys import exit as Sexit
import curses
from curses.textpad import rectangle
import threading
import messagehandler as msgh, lio, exitHandler

def handling_exit():
    if lio.Online: msgh.status(logout=True)
    print("\033[31m" + "You're using inappropriate way to exit." + "\033[0m" + "\n")
    print("Follow me!\033[94m\nGithub: Dzadaafa\nInstagram: Dzadafa\033[0m\nTo get the new update about this project.")
    Sexit()

colors = lio.colors

def main(stdscr):
    global inputUsr, color, username, colors

    curses.start_color()

    for i, colored in enumerate(colors):
        if 2 <= i <= 7:
            curses.init_pair(i + 1, colored, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()

    # Get the screen height and width
    height, width = map(int, stdscr.getmaxyx())
    width = width - 2
    mid_w = int(width/2)

    # List to store the printed numbers
    lines = []

    if username: 
        exitHandler.start(handling_exit)
        lio.Online = True

    while username: #while username exist
        messages = msgh.messages
        online_user = msgh.online_user

        # Check if we have new messages
        while len(messages) > 0:
            new_message = messages.pop(0)
            
            # Check if we have reached the height limit for numbers
            if len(lines) >= height - 6:
                # Remove the oldest number from the top
                lines.pop(0)
            
            # Add the new message to the list
            lines.append(new_message)

        # Clear the screen
        stdscr.clear()

        #BoxDraw
        try:
            rectangle(stdscr, 0, 0, height-5, width)
            rectangle(stdscr, height-4, 0, height-1, mid_w-1)
            rectangle(stdscr, height-4, mid_w+1, height-1, width)
        except Exception as e:
            pass

        #Box 1
        stdscr.addstr(0, mid_w-5, f" TERMTALK ", curses.color_pair(5) | curses.A_UNDERLINE )
        

        for idx, line in enumerate(lines):
            msg, usncolor = line
            usn, usnmsg = msg
            stdscr.addstr(idx + 1, 2, f"{usn}: ", curses.color_pair(usncolor + 1))
            stdscr.addstr(usnmsg)

        #Box3
        stdscr.addstr(height - 4, mid_w + 3, " Key Binding ", curses.color_pair(8))
        stdscr.addstr(height - 2, mid_w + 3, " (Esc) Exit", curses.color_pair(7))
        stdscr.addstr(" | ")
        stdscr.addstr("(Enter) Send ", curses.color_pair(7))

        #Box2
        stdscr.addstr(height - 4, 2, f" Active user: {online_user} ", curses.color_pair(4))
        stdscr.addstr(height - 2, 2, f"-> ", curses.color_pair(3))
        stdscr.addstr(f"{username}: ", curses.color_pair(color + 1))
        stdscr.addstr(str(inputUsr))

        # Refresh the screen to see the changes
        stdscr.refresh()

        # Get user input (non-blocking)
        stdscr.timeout(10)
        key = stdscr.getch()

        # If the user presses 'ESC', break the loop
        if key == 27:
            msgh.status(logout=True)
            lio.Online = False
            lio.logout_screen(stdscr)
            break

        elif key == 8:  # Backspace
            inputUsr = inputUsr[:-1]

        elif key == 10 and len(inputUsr.strip()) >= 1:  # Enter
            sndmsg = msgh.send_message(color, username, inputUsr)
            if sndmsg: inputUsr = ""

        else:
            if key in range(31, 127) and len(inputUsr) <= 30:
                inputUsr = inputUsr + chr(key)

def open_room():
    msgh.status(login=True)
    # Run the message receiving function in a separate thread
    receive_thread = threading.Thread(target=msgh.receive_message, daemon=True)
    receive_thread.start()
    # Initialize curses
    curses.wrapper(main)

def start():
    global username, color
    try:
        username, color = curses.wrapper(lio.main)
    except Exception as e:
        Sexit()
    open_room()
    
username:str
color:int
inputUsr = ""

if __name__=="__main__":
    start()