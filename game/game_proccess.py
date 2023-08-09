import curses
import sys
import termios
import threading
import time
import random
import signal
import shutil

import game
from game.field import Field
from game.player import Player
from game.enemy import Enemy
from game.utils import from_user_to_cage_coordinate

stop_thread = threading.Event()
SCREENSIZE_X, SCREENSIZE_Y = shutil.get_terminal_size()
dspp = 1
while True:
    spp = SCREENSIZE_X//(100//dspp)
    if spp == 0:
        dspp+=1
    else:
        break
spaces = (SCREENSIZE_X-spp*100//dspp)//2
enemies = []

def enemy_handler(pl, fi):
    counter = 0
    while not stop_thread.is_set():
        if counter == 0:
            enemies.append(Enemy("Z", random.randint(-15, 14), random.randint(-7, 7), fi))
        for en in enemies:
            if en.health<=0:
                fi.set_enemy(*en.get_pos())
                time.sleep(0.1)
                fi.deactivate_by_non_player(*en.get_pos())
                enemies.remove(en)
                if len(enemies) == 0:
                    time.sleep(10)
                    enemies.append(Enemy("Z", random.randint(-15, 14), random.randint(-7, 7), fi))
                continue    
            counter = (counter+1)%10
            time.sleep((0.4)/len(enemies))
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
    pl = Player("@", 0, 0, fi)
    fi.set_player(*pl.get_pos())
    player_coords = pl.get_pos()
    curses.curs_set(0)
    win = curses.newwin(SCREENSIZE_Y, SCREENSIZE_X, 0,0)
    enemy_thread = threading.Thread(target=enemy_handler, args=(pl, fi))
    enemy_thread.start()

    def handle_resize(window, signum, frame):
        global SCREENSIZE_X, SCREENSIZE_Y, spp, spaces, dspp
        curses.endwin()
        curses.initscr()
        SCREENSIZE_X, SCREENSIZE_Y = shutil.get_terminal_size()
        dspp = 1
        while True:
            spp = SCREENSIZE_X//(100//dspp)
            if spp == 0:
                dspp+=1
            else:
                break
        spaces = (SCREENSIZE_X-spp*100//dspp)//2
        win = curses.newwin(SCREENSIZE_Y, SCREENSIZE_X)
        win.refresh()


    signal.signal(signal.SIGWINCH, lambda s, f: handle_resize(win, s, f))
    while True:
        # Get the character
        win.nodelay(True)
        char = win.getch()
        #win.refresh()
        match char:
            case game.W_KEY:
                pl.move("up")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("down")
                    pl.direction = "up"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.A_KEY:
                pl.move("left")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("right")
                    pl.direction = "left"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.S_KEY:
                pl.move("down")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("up")
                    pl.direction = "down"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.D_KEY:
                pl.move("right")
                player_coords = pl.get_pos()
                if fi.set_player(*player_coords) == 0:
                    pl.move("left")
                    pl.direction = "right"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.SPACE_KEY:
                pl.attack()
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.ENTER_KEY:
                is_chest = False
                for x in range(player_coords[1], player_coords[1]+1):
                    for y in range(player_coords[2], player_coords[2]+1):
                        sym = fi.get_cage_by_coords((x, y))[0]
                        if sym == "+":
                            is_chest = True
                            break
                if is_chest:
                    area_id, _ = from_user_to_cage_coordinate(player_coords[1:])
                    pl.change_weapon(fi.change_weapon(area_id, pl.level, pl.weapon))

            case game.ESC_KEY:
                stop_thread.set()
                return
            #case _:
            #    print(char)
        if pl.attack_stage:
            pl.attack()
        win.addstr(0, 0, f"({player_coords[1]}, {player_coords[2]}, {counter})")
        counter+=1
        try:
            win.addstr(1,0, f"{pl.get_exp()[0]} LVL {pl.get_exp()[1]}/{pl.get_exp()[2]}")
            win.addstr(2,0, " "*((SCREENSIZE_X-7)//2) + "YOUR HP")
            win.addstr(4, 0, f"Текущее оружие: {str(pl.weapon)}")
            win.addstr(4, len(f"Текущее оружие: {str(pl.weapon)}"), " "*(SCREENSIZE_X-len(f"Текущее оружие: {str(pl.weapon)}")))
        except Exception:
            pass
        if pl.get_health() <=0:
            return
        win.addstr(3,0, " "*spaces+"["+"#"*(spp*pl.get_health()//dspp)+" "*(spp*(100 - pl.get_health())//dspp)+"]")
        try:
            for x in range(SCREENSIZE_X-1):
                for y in range(5, SCREENSIZE_Y):
                    showing_coord = (pl.get_pos()[1]+SCREENSIZE_X//2-x, pl.get_pos()[2]+SCREENSIZE_Y//2-y)
                    sym, enemy = fi.get_cage_by_coords(showing_coord)
                    if enemy:
                        for en in filter(lambda eni: (eni.get_pos()[1], eni.get_pos()[2]) == showing_coord, enemies):
                            prize_exp = en.get_damage(pl.damage)
                            if prize_exp:
                                pl.add_exp(prize_exp)    
                    win.addstr(y, x, sym)
        except:
            with open("nohup.out", "a", encoding = "UTF-8") as file:
                file.write(f"{x} {y} {SCREENSIZE_Y} {SCREENSIZE_X}\n {exec}\n")
        win.refresh()     
        time.sleep(0.03)
if __name__ == "__main__":
    curses.wrapper(start)
    stop_thread.set()
    print("GAME_OVER")

