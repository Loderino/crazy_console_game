import json
import time
from game import USER_CONFIGS, LEVELS
from game.weapon import Weapon
class Player:
    level = 0
    kills = 0
    exp = 0
    attack_stage = 0
    direction = "up"
    player_configs={}
    levels = {}
    def __init__(self, sym, x_coordinate, y_coordinate, fi):
        self.__sym = sym
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.fi = fi
        with open(USER_CONFIGS, "r", encoding = "UTF-8") as file:
            self.player_configs = json.load(file)
            self.max_health = self.player_configs["max_health"]
            self.health = self.player_configs["max_health"]
            self.attack_k = self.player_configs["attack"]
            self.speed = 1
        with open(LEVELS, "r", encoding = "UTF-8") as file:
            self.levels = json.load(file)
        self.weapon = Weapon("Палка", "D", "", 1)
        self.damage = self.attack_k*self.weapon.get_information()[0]

    def increase_param(self, param, value):
        match param:
            case "health":
                self.max_health+=value
            case "attack":
                self.attack_k+=value
            case "speed":
                self.speed+=value
    def move(self, direction):
        match direction:
            case "up":
                self.__y_coordinate+=self.speed
            case "down":
                self.__y_coordinate-=self.speed
            case "right":
                self.__x_coordinate-=self.speed
            case "left":
                self.__x_coordinate+=self.speed
        self.direction=direction
    def get_pos(self):
        return (self.__sym, self.__x_coordinate, self.__y_coordinate)
    
    def get_health(self):
        return int(self.health/self.max_health*100)
    
    def regeneration(self):
        self.health+=self.max_health*0.25
        if self.health>self.max_health:
            self.health = self.max_health
    
    def get_damage(self, damage):
        self.health -= damage*(100-self.player_configs["defense"])//100

    def attack(self):
        
        match(self.weapon.length):
            case 1:
                if self.direction in ["up", "right"]:
                    match self.attack_stage:
                        case 0:
                            self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                        case 1:
                            self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate+1)
                        case 2:
                            self.fi.set_effect("/", self.__x_coordinate-1, self.__y_coordinate+1)
                        case 3:  
                            self.fi.set_effect("-", self.__x_coordinate-1, self.__y_coordinate)
                        case 4:
                            self.fi.set_effect("_", self.__x_coordinate-1, self.__y_coordinate)
                        case 5:
                            self.fi.set_effect("\\", self.__x_coordinate-1, self.__y_coordinate-1)
                            self.attack_stage = -1
                else:
                    match self.attack_stage:
                        case 0:
                            self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                        case 1:
                            self.fi.set_effect("-", self.__x_coordinate+1, self.__y_coordinate)
                        case 2:  
                            self.fi.set_effect("_", self.__x_coordinate+1, self.__y_coordinate)
                        case 3:  
                            self.fi.set_effect("/", self.__x_coordinate+1, self.__y_coordinate-1)
                        case 4:
                            self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate-1)
                        case 5:
                            self.fi.set_effect("\\", self.__x_coordinate-1, self.__y_coordinate-1)
                            self.attack_stage = -1
            case 2:
                if self.direction in ["up", "right"]:
                    lines = ["\\", "|", "|", "/", "/", "-", '_', "\\", "\\"]
                    what_sym = lambda x, stage: lines[stage] if x=="|" else x
                    match self.attack_stage:
                        case 0:
                            self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 0), self.__x_coordinate+2, self.__y_coordinate+2)
                        case 1:
                            self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 1), self.__x_coordinate+1, self.__y_coordinate+2)
                        case 2:
                            self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 2), self.__x_coordinate, self.__y_coordinate+2)
                        case 3:  
                            self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 3), self.__x_coordinate-1, self.__y_coordinate+2)
                        case 4:
                            self.fi.set_effect("/", self.__x_coordinate-1, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 4), self.__x_coordinate-2, self.__y_coordinate+2)
                        case 5:
                            self.fi.set_effect("/", self.__x_coordinate-1, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 5), self.__x_coordinate-2, self.__y_coordinate+1)
                        case 6:
                            self.fi.set_effect("-", self.__x_coordinate-1, self.__y_coordinate)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 6), self.__x_coordinate-2, self.__y_coordinate)
                        case 7:
                            self.fi.set_effect("_", self.__x_coordinate-1, self.__y_coordinate)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 7), self.__x_coordinate-2, self.__y_coordinate-1)
                        case 8:
                            self.fi.set_effect("\\", self.__x_coordinate-1, self.__y_coordinate-1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 8), self.__x_coordinate-2, self.__y_coordinate-2)
                            self.attack_stage = -1
                else:
                    lines = ["\\", "-", "-", "/", "/", "|", '|', "\\", "\\"]
                    what_sym = lambda x, stage: lines[stage] if x=="|" else x
                    match self.attack_stage:
                        case 0:
                            self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 0), self.__x_coordinate+2, self.__y_coordinate+2)
                        case 1:
                            self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 1), self.__x_coordinate+2, self.__y_coordinate+1)
                        case 2:
                            self.fi.set_effect("-", self.__x_coordinate+1, self.__y_coordinate)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 2), self.__x_coordinate+2, self.__y_coordinate)
                        case 3:  
                            self.fi.set_effect("_", self.__x_coordinate+1, self.__y_coordinate)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 3), self.__x_coordinate+2, self.__y_coordinate-1)
                        case 4:
                            self.fi.set_effect("/", self.__x_coordinate+1, self.__y_coordinate-1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 4), self.__x_coordinate+2, self.__y_coordinate-2)
                        case 5:
                            self.fi.set_effect("/", self.__x_coordinate+1, self.__y_coordinate-1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 5), self.__x_coordinate+1, self.__y_coordinate-2)
                        case 6:
                            self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate-1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 6), self.__x_coordinate, self.__y_coordinate-2)
                        case 7:
                            self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate-1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 7), self.__x_coordinate-1, self.__y_coordinate-2)
                        case 8:
                            self.fi.set_effect("\\", self.__x_coordinate-1, self.__y_coordinate-1)
                            self.fi.set_effect(what_sym(self.weapon.get_information()[2], 8), self.__x_coordinate-2, self.__y_coordinate-2)
                            self.attack_stage = -1

        self.attack_stage+=1

    def add_exp(self, exp_num):
        self.exp+=exp_num
        try:
            if self.exp>=self.levels[str(self.level+1)]:
                self.level+=1
                self.exp-=self.levels[str(self.level)]
        except KeyError:
            pass
    
    def get_exp(self):
        return (self.level,self.exp, self.levels.get(str(self.level+1), "∞"))
    
    def change_weapon(self, wep):
        self.weapon = wep
        self.damage = self.attack_k*self.weapon.get_information()[0]
