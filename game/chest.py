import json
import random
from game.weapon import Weapon
from game import WEAPON_DICT
class Chest:
    def __init__(self, ID):
        self.ID = ID
        self.is_open = False

    def open(self, lvl):
        self.is_open = True
        with open(WEAPON_DICT, "r", encoding = "UTF-8") as file:
            weapons = json.load(file)

        names = list(weapons.keys())
        random.shuffle(names)
        name = names[0]
        chance = random.randint(0, 1000)
        if chance in range(0, 500):
            rank = "D"
        elif chance in range(500, 700+3*lvl):
            rank = "C"
        elif chance in range(700+3*lvl, 800+2*lvl):
            rank = "B"
        elif chance in range(800+2*lvl, 900+lvl):
            rank = "A"
        elif chance in range(900+lvl, 980-lvl):
            rank = "S"
        else:
            rank = "SSS"
        self.value = Weapon(name, rank, weapons[name]["anim"], int(weapons[name]["length"]))

    def change_value(self, wep):
        ch_weapon = self.value
        self.value = wep
        return ch_weapon
    
