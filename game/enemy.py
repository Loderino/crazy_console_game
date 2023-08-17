import random
class Enemy:
    pause = False
    counter = 0
    health = 100
    defense = 0
    speed = 1
    attack = 5
    def __init__(self, sym, x_coordinate, y_coordinate, fi):
        self.__sym = sym
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.fi = fi
        self.prize_exp = self.health//100+self.defense//10+self.attack//5 + self.speed

    def get_pos(self):
        return (self.__sym, self.__x_coordinate, self.__y_coordinate)
    
    def move(self, player_pos):
        if not self.pause and self.health>0:
            changing_pos = ""
            if (abs(player_pos[1]-self.__x_coordinate) > abs(player_pos[2]-self.__y_coordinate)):
                if self.__x_coordinate < player_pos[1]:
                    self.__x_coordinate += self.speed
                    changing_pos = "x+"
                if self.__x_coordinate > player_pos[1]:
                    self.__x_coordinate -= self.speed
                    changing_pos = "x-"
            else:
                if self.__y_coordinate < player_pos[2]:
                    self.__y_coordinate += self.speed
                    changing_pos = "y+"
                if self.__y_coordinate > player_pos[2]:
                    self.__y_coordinate -= self.speed
                    changing_pos = "y-"
            counter = 0
            directions = ("x", "y", "+", "-")
            while self.fi.get_cage_by_coords((self.__x_coordinate, self.__y_coordinate))[0] not in  (".", " "):
                match changing_pos:
                    case "x+":
                        self.__x_coordinate-=self.speed
                        if counter == 3:
                            break
                    case "x-":
                        self.__x_coordinate+=self.speed
                        if counter == 3:
                            break
                    case "y+":
                        self.__y_coordinate-=self.speed
                        if counter == 3:
                            break
                    case "y-":
                        self.__y_coordinate+=self.speed
                        if counter == 3:
                            break
                changing_pos = f"{directions[random.randint(0,1)]}{directions[random.randint(2,3)]}"
                if changing_pos[0] == "x":
                    if changing_pos[1] == "+":
                        self.__x_coordinate+=self.speed
                    else:
                        self.__x_coordinate-=self.speed
                else:
                    if changing_pos[1] == "+":
                        self.__y_coordinate+=self.speed
                    else:
                        self.__y_coordinate-=self.speed

                counter+=1
        return self.get_pos()
    
    def kick(self):
        if not self.pause and self.health>0 :
            self.pause = True
            return self.attack
        
    def check_for_player(self, player_coords):
        if not self.pause:
            if abs(self.__x_coordinate - player_coords[1])<=1 and abs(self.__y_coordinate - player_coords[2])<=1:
                return self.kick()
        else:
            self.counter+=1
            if self.counter >= 25:
                self.pause = False
                self.counter = 0
            return "stop"

    def get_damage(self, damage):
        self.health-=(damage*(100-self.defense)//100)
        if self.health<=0 and self.health+damage>0:
           self.__sym = "0"
           self.pause = False 
           self.counter = 0
           return self.prize_exp