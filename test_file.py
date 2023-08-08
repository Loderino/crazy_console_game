import os
import curses
import time
import signal

def start(stdscr):
    while True:
        char = stdscr.getch()
        print(char)

if __name__ == "__main__":
    curses.wrapper(start)