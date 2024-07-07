import curses
from random import randint

title = r"""
  ______                   _        _ _    
  |_   _|                 | |      | | |   
    | | ___ _ __ _ __ ___ | |_ __ _| | | __
    | |/ _ \ '__| '_ ` _ \| __/ _` | | |/ /
    | |  __/ |  | | | | | | || (_| | |   < 
    \_/\___|_|  |_| |_| |_|\__\__,_|_|_|\_\
    ───────────── By Dzadafa ───────────── 
                                          
    

"""


def main(stdscr):
  username = ""
  # stdscr.clear()
  height, width = map(int, stdscr.getmaxyx())

  title_line = title.count('\n')


  while True:
    stdscr.clear()
    stdscr.addstr(0,0, title)
    stdscr.addstr(title_line, 0, "Press (Esc) to Cancel", curses.A_ITALIC)
    stdscr.addstr(title_line + 1, 0, "Username: " + username)
    stdscr.refresh()
    key = stdscr.getch()


    if key == 10 and username.strip():
      return (username, randint(2, 7))
    elif key == 27:
            break
    elif key == 8:
      username = username[:-1]
    else:
      if (key in range(64, 91) or key in range(97, 123)) and len(username) <= 8:
        username = username + chr(key)


if __name__ == "__main__":
  curses.wrapper(main)