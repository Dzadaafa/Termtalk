from sys import exit as Sexit
from time import sleep
import curses
from random import randint, uniform
import exitHandler

Online = False

def cleanup_and_exit():
    print("\033[31m" + "You're using inappropriate way to exit." + "\033[0m" + "\n")
    Sexit()

exitHandler.start(cleanup_and_exit)

title = r"""
   _____                   _        _ _    
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
      stdscr.addstr(title_line + 2, 0, "(Esc) Exit || (Enter) Submit", curses.A_ITALIC)
      stdscr.addstr(title_line + 3, 0, "-> Username: " + username)
      stdscr.refresh()

      key = stdscr.getch()

      if key == 8:
          username = username[:-1]
      elif key == 10:
          if len(username) >= 3:
            return username
          else:
            min_char = " (Min. 3 char)"
      elif key == 27:
          break
      else:
        if (key in range(64, 91) or key in range(97, 123)) and len(username) <= 8:
          username = username + chr(key)
      
# stdscr
def logout_screen(stdscr) -> None:
    text = "Closing program..."
    stdscr.clear()
    stdscr.addstr(0, 0, text)
    # stdscr.addstr(1, 0, "")
    stdscr.addstr(2, 0, "Follow me!")
    stdscr.addstr(3, 0, "Github: Dzadaafa | Instagram: Dzadafa", curses.color_pair(8))

    for num, txt in enumerate(text):
      stdscr.refresh()
      stdscr.addstr(0, num, txt, curses.color_pair(3))
      sleep(uniform(0.1, 0.5))

    stdscr.addstr(0, 0, "Done" + " " * len(text), curses.color_pair(3))
    stdscr.refresh()
    sleep(1)
    stdscr.getch()


def main(stdscr) -> list | None:
  # stdscr.clear()
  height, width = map(int, stdscr.getmaxyx())
  min_height, min_width = (15, 65)

  if height <= min_height and width <= min_width:
      print("\033[31m" + "Expand your terminal height and width."+"\033[33m")
      print(f"Mininum: {min_height} x {min_width}" + f"\nYours: {height} x {width}" + "\033[0m") 
      return
  elif width <= min_width:
      print("\033[31m" + "Expand your terminal width." + "\033[33m")
      print(f"Minimum: {min_width}"  + f"\nYours: {width}"+ "\033[0m")
      return
  elif height <= min_height:
      print("\033[31m" + "Expand your terminal height." + "\033[33m")
      print(f"Minimum: {min_height}" + f"\nYours: {height}"+ "\033[0m")
      return

  username = username_input(stdscr)
  
  if username:
    color = color_pick(stdscr, username)
  else:
    return
  
  if color:
    stdscr.clear()
    return (username, color)

if __name__ == "__main__":
  # curses.wrapper(main)
  curses.wrapper(logout_screen)