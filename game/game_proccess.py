import json
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
from game.skills_tab import Skills_tab
from game.utils import from_user_to_cage_coordinate


status = "game"
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
fi = Field()
pl = Player("@", 0, 0, fi)
skills_tab = Skills_tab(pl)

with open(game.ENEMY_SCALE) as file:
    enemy_range = json.load(file) 

def create_enemy():
    global fi, pl
    enemies_types = []
    power_level = (pl.level*5+pl.kills*5)*pl.attack_k*10
    for key in enemy_range.keys():
        if int(key)<=power_level:
            enemies_types.append(key)
        else:
            break
    p = random.randint(0, int(enemies_types[-1]))
    selected_type = min(enemies_types, key = lambda x: abs(p-int(x)))
    
    en = Enemy(enemy_range[selected_type]["sym"], random.randint(-15, 14), random.randint(-7, 7), fi)
    en.attack = enemy_range[selected_type]["attack"]
    en.speed = enemy_range[selected_type]["speed"]
    en.defense = enemy_range[selected_type]["defense"]
    en.health = enemy_range[selected_type]["health"]
    return en

        


def enemy_handler(pl, fi):
    counter = 0
    while not stop_thread.is_set():
        if status == "game":
            if counter == 0 and len(enemies)<20:
                enemies.append(create_enemy())
            for en in enemies:
                if en.health<=0:
                    fi.set_enemy(*en.get_pos())
                    time.sleep(0.1)
                    fi.deactivate_by_non_player(*en.get_pos())
                    enemies.remove(en)
                    if len(enemies) == 0:
                        time.sleep(10)
                        enemies.append(create_enemy())
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
    global status
    counter=0
    fi.set_player(*pl.get_pos())
    player_coords = pl.get_pos()
    curses.curs_set(0)
    curses.start_color()
    #curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
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
                if status == "game":
                    pl.move("up")
                    player_coords = pl.get_pos()
                    if fi.set_player(*player_coords) == 0:
                        pl.move("down")
                        pl.direction = "up"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.A_KEY:
                if status == "game":
                    pl.move("left")
                    player_coords = pl.get_pos()
                    if fi.set_player(*player_coords) == 0:
                        pl.move("right")
                        pl.direction = "left"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.S_KEY:
                if status == "game":
                    pl.move("down")
                    player_coords = pl.get_pos()
                    if fi.set_player(*player_coords) == 0:
                        pl.move("up")
                        pl.direction = "down"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.D_KEY:
                if status == "game":
                    pl.move("right")
                    player_coords = pl.get_pos()
                    if fi.set_player(*player_coords) == 0:
                        pl.move("left")
                        pl.direction = "right"
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.SPACE_KEY:
                if status == "game":
                    pl.attack()
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            case game.ENTER_KEY:
                if status == "game":
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
            case game.TAB_KEY:
                if status == "game":
                    status = "skills"
                elif status == "skills":
                    status = "game"
            case game.ONE_KEY:
                if status =="skills":
                    skills_tab.increase_skill("regeneration")
            case game.TWO_KEY:
                if status == "skills":
                    skills_tab.increase_skill("health")
            case game.THREE_KEY:
                if status == "skills":
                    skills_tab.increase_skill("attack")
            case game.FOUR_KEY:
                if status == "skills":
                    skills_tab.increase_skill("speed")
            case game.ESC_KEY:
                stop_thread.set()
                return
            #case _:
            #    print(char)
        if status == "game":
            if pl.attack_stage:
                pl.attack()
            win.addstr(0, 0, f"({player_coords[1]}, {player_coords[2]}){' ' * (SCREENSIZE_X-len(str(player_coords[2])+str(player_coords[1]))-2)}")
            counter+=1
            try:
                win.addstr(1,0, f"{pl.get_exp()[0]} LVL {pl.get_exp()[1]}/{pl.get_exp()[2]}, KILLS: {pl.kills}     ")
                win.addstr(1, SCREENSIZE_X-2, " ")
                win.addstr(2,0, " "*((SCREENSIZE_X-7)//2) + "YOUR HP" + " "*((SCREENSIZE_X-7)//2))
                win.addstr(4, 0, f"Текущее оружие: {str(pl.weapon)}")
                win.addstr(4, len(f"Текущее оружие: {str(pl.weapon)}"), " "*(SCREENSIZE_X-len(f"Текущее оружие: {str(pl.weapon)}")))
            except Exception:
                pass
            if pl.get_health() <=0:
                return
            win.addstr(3,0, " "*spaces+"["+"#"*(spp*pl.get_health()//dspp)+" "*(spp*(100 - pl.get_health())//dspp)+"]"+" "*(spaces-2))
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
                                    pl.kills+=1
                                    if pl.kills%10 == 0:
                                        skills_tab.points+=1
                        if sym == player_coords[0]:    
                            win.addstr(y, x, sym, curses.color_pair(2))
                        elif sym.isalpha():
                            win.addstr(y, x, sym, curses.color_pair(1))
                        else:
                            win.addstr(y, x, sym)
            except:
                with open("nohup.out", "a", encoding = "UTF-8") as file:
                    file.write(f"{x} {y} {SCREENSIZE_Y} {SCREENSIZE_X}\n {exec}\n")

        elif status == "skills":
            tab = skills_tab.get_tab(SCREENSIZE_X, SCREENSIZE_Y)
            win.addstr(0, 0, tab)
        win.refresh()     
        time.sleep(0.03)
if __name__ == "__main__":
    curses.wrapper(start)
    stop_thread.set()
    print("GAME_OVER")

