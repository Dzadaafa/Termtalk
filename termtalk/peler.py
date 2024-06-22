import argparse
from time import sleep as turu
import os
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--sort", help="print s? idk", action="store_true")
parser.add_argument("-d", "--decrypt", help="deez what?", action="store_true")

arg = parser.parse_args()

def ajg():
  if arg.sort:
    os.execl(sys.executable, sys.executable, "alr.py")
  elif arg.decrypt:
    print("anjing")
  else:
    print("without argparse")

if __name__ == "__main__":
  ajg()

