class Player:
    def __init__(self, sym, x_coordinate, y_coordinate):
        self.__sym = sym
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
    def move(self, direction):
        match direction:
            case "up":
                self.__y_coordinate+=1
            case "down":
                self.__y_coordinate-=1
            case "right":
                self.__x_coordinate-=1
            case "left":
                self.__x_coordinate+=1
    def get_pos(self):
        return (self.__sym, self.__x_coordinate, self.__y_coordinate)