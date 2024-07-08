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
title_line = title.count('\n')

colors = [
    curses.COLOR_BLACK, curses.COLOR_WHITE,
    curses.COLOR_CYAN, curses.COLOR_GREEN,
    curses.COLOR_MAGENTA, curses.COLOR_RED,
    curses.COLOR_BLUE, curses.COLOR_YELLOW
]

def color_pick(stdscr, username) -> int:
    global colors

    color = 2
    curses.start_color()

    if not curses.has_colors():
      stdscr.addstr(0, 0, "Your terminal does not support colors.", curses.A_BOLD)
      stdscr.refresh()
      stdscr.getch()
      return 3

    for i, colored in enumerate(colors):
        if 2 <= i <= 7:
            curses.init_pair(i + 1, colored, curses.COLOR_BLACK)

    while True:
      stdscr.clear()
      stdscr.addstr(0,0, title, curses.color_pair(color+1))
      stdscr.addstr(title_line, 0, "--Pick a color")
      stdscr.addstr(title_line + 1, 0, "(Esc) Exit | (Enter) Submit | (C) Choose | (R) Randomize ", curses.A_ITALIC)
      stdscr.addstr(title_line + 2, 0, f"-> {username} : ", curses.color_pair(color+1))
      stdscr.addstr("This is Preview")
      stdscr.refresh()

      key = stdscr.getch()

      if key == 10:
          return color
      elif key == 27:
          break
      elif key == ord("r") or key == ord("R"):
          return randint(2, 7)
      elif key == ord("c") or key == ord("C"):
          color = color + 1 if color < 7 else 2


def username_input(stdscr) -> str:
    username = ""
    min_char = ""

    while True:
      stdscr.clear()
      stdscr.addstr(0,0, title)
      stdscr.addstr(title_line, 0, "--Input your username" + min_char)
      stdscr.addstr(title_line + 1, 0, "(Esc) Exit | (Enter) Submit", curses.A_ITALIC)
      stdscr.addstr(title_line + 2, 0, "Username: " + username)
      stdscr.refresh()

      key = stdscr.getch()

      if key == 8:
          username = username[:-1]
      elif key == 10:
          if len(username) >= 3:
            return username
          else:
            min_char = "(Min. 3 char)"
      elif key == 27:
          break
      else:
        if (key in range(64, 91) or key in range(97, 123)) and len(username) <= 8:
          username = username + chr(key)
      



def main(stdscr) -> list | None:
  # stdscr.clear()
  height, width = map(int, stdscr.getmaxyx())

  if height <= title_line + 3 and width <= 50:
      print("\033[33m" + "Expand your terminal height and width." + "\033[0m")
      return
  elif width <= 50:
      print("\033[33m" + "Expand your terminal width." + "\033[0m")
      return
  elif height <= title_line + 3:
      print("\033[33m" + "Expand your terminal height." + "\033[0m")
      return

  username = username_input(stdscr)
  
  if username:
    color = color_pick(stdscr, username)
  else:
    return
  
  if color:
    return (username, color)

if __name__ == "__main__":
  curses.wrapper(main)