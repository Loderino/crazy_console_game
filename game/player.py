import json
import time
from game import USER_CONFIGS
from game import field
class Player:
    attack_stage = 0
    direction = "up"
    player_configs={}
    def __init__(self, sym, x_coordinate, y_coordinate, fi):
        self.__sym = sym
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.fi = fi
        with open(USER_CONFIGS, "r", encoding = "UTF-8") as file:
            self.player_configs = json.load(file)
        self.health = self.player_configs["max_health"]
        self.damage = self.player_configs["attack"]
    def move(self, direction):
        match direction:
            case "up":
                self.__y_coordinate+=self.player_configs["speed"]
            case "down":
                self.__y_coordinate-=self.player_configs["speed"]
            case "right":
                self.__x_coordinate-=self.player_configs["speed"]
            case "left":
                self.__x_coordinate+=self.player_configs["speed"]
        self.direction=direction
    def get_pos(self):
        return (self.__sym, self.__x_coordinate, self.__y_coordinate)
    
    def get_health(self):
        return int(self.health/self.player_configs["max_health"]*100)
    
    def get_damage(self, damage):
        self.health -= damage*(100-self.player_configs["defense"])//100

    def attack(self):
        if self.direction in ["up", "right"]:
            match self.attack_stage:
                case 0:
                    # \ 
                    #  @
                    self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                case 1:
                    # | 
                    # @
                    self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate+1)
                case 2:
                    #  / 
                    # @ 
                    self.fi.set_effect("/", self.__x_coordinate-1, self.__y_coordinate+1)
                case 3:  
                    # @-
                    self.fi.set_effect("-", self.__x_coordinate-1, self.__y_coordinate)
                case 4:
                    # @_  
                    self.fi.set_effect("_", self.__x_coordinate-1, self.__y_coordinate)
                case 5:
                    # @
                    #  \
                    self.fi.set_effect("\\", self.__x_coordinate-1, self.__y_coordinate-1)
                    self.attack_stage = -1
        else:
            match self.attack_stage:
                case 0:
                    #\ 
                    # @
                    self.fi.set_effect("\\", self.__x_coordinate+1, self.__y_coordinate+1)
                case 1:
                    # -@
                    self.fi.set_effect("-", self.__x_coordinate+1, self.__y_coordinate)
                case 2: 
                    # _@ 
                    self.fi.set_effect("_", self.__x_coordinate+1, self.__y_coordinate)
                case 3:  
                    # @
                    #/
                    self.fi.set_effect("/", self.__x_coordinate+1, self.__y_coordinate-1)
                case 4:
                    # @
                    # |  
                    self.fi.set_effect("|", self.__x_coordinate, self.__y_coordinate-1)
                case 5:
                    # @
                    #  \
                    self.fi.set_effect("\\", self.__x_coordinate-1, self.__y_coordinate-1)
                    self.attack_stage = -1
        self.attack_stage+=1

