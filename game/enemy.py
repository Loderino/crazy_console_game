class Enemy:
    pause = False
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
        if not self.pause:
            if (abs(player_pos[1]-self.__x_coordinate) > abs(player_pos[2]-self.__y_coordinate)):
                if self.__x_coordinate < player_pos[1]:
                    self.__x_coordinate += self.speed
                    return self.get_pos()
                if self.__x_coordinate > player_pos[1]:
                    self.__x_coordinate -= self.speed
                    return self.get_pos()
            else:
                if self.__y_coordinate < player_pos[2]:
                    self.__y_coordinate += self.speed
                    return self.get_pos()
                if self.__y_coordinate > player_pos[2]:
                    self.__y_coordinate -= self.speed
                    return self.get_pos()
        self.pause = False
        return self.get_pos()
    
    def kick(self):
        if not self.pause:
            return self.attack
        else:
            self.pause = False
            return 0
        
    def check_for_player(self, player_coords):
        if abs(self.__x_coordinate - player_coords[1])<=1 and abs(self.__y_coordinate - player_coords[2])<=1:
            return self.kick()