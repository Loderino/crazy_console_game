class Enemy:
    pause = False
    counter = 0
    health = 100
    defense = 20
    speed = 1
    attack = 5
    def __init__(self, sym, x_coordinate, y_coordinate):
        self.__sym = sym
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate

    def get_pos(self):
        return (self.__sym, self.__x_coordinate, self.__y_coordinate)
    
    def move(self, player_pos):
        if not self.pause and self.health>0:
            if (abs(player_pos[1]-self.__x_coordinate) > abs(player_pos[2]-self.__y_coordinate)):
                if self.__x_coordinate < player_pos[1]:
                    self.__x_coordinate += self.speed
                if self.__x_coordinate > player_pos[1]:
                    self.__x_coordinate -= self.speed
            else:
                if self.__y_coordinate < player_pos[2]:
                    self.__y_coordinate += self.speed
                if self.__y_coordinate > player_pos[2]:
                    self.__y_coordinate -= self.speed
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
        self.health-=damage
        self.__sym = "K"
        if self.health<=0:
           self.__sym = "X"
           self.pause = False 
           self.counter = 0