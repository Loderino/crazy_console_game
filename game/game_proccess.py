import curses
import time
import sys
import termios

import game
from game.field import Field
from game.player import Player
from game.utils import from_user_to_cage_coordinate

def start(stdscr):
    fi = Field()
    pl = Player("@", 0, 0)
    fi.set_player(0,0)
    curses.curs_set(0)
    win = curses.newwin(70, 210, 0, 0)
    
    while True:
        # Get the character
        char = win.getch()
        win.refresh()
        match char:
            case game.W_KEY:
                pl.move("up")
                player_coords = pl.get_pos()
                fi.set_player(player_coords[1], player_coords[2])
            case game.A_KEY:
                pl.move("left")
                player_coords = pl.get_pos()
                fi.set_player(player_coords[1], player_coords[2])
            case game.S_KEY:
                pl.move("down")
                player_coords = pl.get_pos()
                fi.set_player(player_coords[1], player_coords[2])
            case game.D_KEY:
                pl.move("right")
                player_coords = pl.get_pos()
                fi.set_player(player_coords[1], player_coords[2])
            case _:
                print(char)

        win.addstr(0, 0, f"({player_coords[1]}, {player_coords[2]}")
        for x in range(0, game.SCREENSIZE_X+1):
            for y in range(4, game.SCREENSIZE_Y+1):
                showing_coord = (pl.get_pos()[1]+game.SCREENSIZE_X//2-x, pl.get_pos()[2]+game.SCREENSIZE_Y//2-y)
                win.addstr(y, x, fi.get_cage_by_coords(showing_coord))
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)         

if __name__ == "__main__":
    curses.wrapper(start)


