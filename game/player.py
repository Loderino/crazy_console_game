import json
from game import USER_CONFIGS

class Player:
    direction = "up"
    player_configs={}
    def __init__(self, sym, x_coordinate, y_coordinate):
        self.__sym = sym
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        with open(USER_CONFIGS, "r", encoding = "UTF-8") as file:
            self.player_configs = json.load(file)
        self.health = self.player_configs["max_health"]
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