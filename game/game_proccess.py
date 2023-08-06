import curses
import sys
import termios
import threading
import time
import random

import game
from game.field import Field
from game.player import Player
from game.enemy import Enemy

stop_thread = threading.Event()

def enemy_handler(pl, fi):
    enemies = []
    enemies.append(Enemy("Z", 10, 0))
    enemies.append(Enemy("Z", random.randint(-15, 14), random.randint(-15, 14)))
    while not stop_thread.is_set():
        for en in enemies:    
            time.sleep(0.2)
            damage = en.check_for_player(pl.get_pos())
            if not damage:
                fi.deactivate_by_non_player(*en.get_pos())
                en.move(pl.get_pos())
                fi.set_enemy(*en.get_pos())
            elif damage == "stop":
                pass
            else:
                if pl.get_damage(damage):
                    stop_thread.set()
                    return    
def start(stdscr):
    counter=0
    fi = Field()
    pl = Player("@", 0, 0)
    fi.set_player(*pl.get_pos())
    player_coords = pl.get_pos()
    curses.curs_set(0)
    win = curses.newwin(70, 210, 0,0)
    enemy_thread = threading.Thread(target=enemy_handler, args=(pl, fi))
    enemy_thread.start()
    while True:
        # Get the character
        win.nodelay(True)
        char = win.getch()
        win.refresh()
        match char:
            case game.W_KEY:
                pl.move("up")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("down")
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.A_KEY:
                pl.move("left")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("right")
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.S_KEY:
                pl.move("down")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("up")
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.D_KEY:
                pl.move("right")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("left")
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.ESC_KEY:
                stop_thread.set()
                return
            #case _:
            #    print(char)

        win.addstr(0, 0, f"({player_coords[1]}, {player_coords[2]}, {counter})")
        counter+=1
        win.addstr(1,100, "YOUR HP")
        if pl.get_health() <=0:
            return
        win.addstr(2,1, "["+"#"*2*pl.get_health()+" "*2*(100 - pl.get_health())+"]")
        for x in range(0, game.SCREENSIZE_X+1):
            for y in range(4, game.SCREENSIZE_Y+1):
                showing_coord = (pl.get_pos()[1]+game.SCREENSIZE_X//2-x, pl.get_pos()[2]+game.SCREENSIZE_Y//2-y)
                win.addstr(y, x, fi.get_cage_by_coords(showing_coord))        
        time.sleep(0.03)
if __name__ == "__main__":
    curses.wrapper(start)
    stop_thread.set()
    print("GAME_OVER")

