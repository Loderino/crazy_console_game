from game.utils import from_user_to_cage_coordinate
import random
class Cage:
    """Класс клетки (один символ в консоли)"""
    active = False
    __sym = "."
    def __init__(self, x, y):
        """конструктор
        Args:
            x - координата по ширине в зоне
            y - координата по высоте в зоне
        """
        self.__x_coordinate = x
        self.__y_coordinate = y
    def __str__(self):
        """Метод для перевода в str"""
        return f"({self.__x_coordinate}; {self.__y_coordinate})"
    
    def activate(self, sym, initiator = "player"):
        """Метод активации клетки. Изменяет её символ, когда на неё находится игрок"""
        match initiator:
            case "player":
                self.active = True
                self.__sym = sym
            case "enemy":
                self.active = True
                self.__sym = sym    

    def deactivate(self):
        """Метод деактивации. Возвращает стандартный вид, когда игрок уходит с неё"""
        self.active = False
        self.__sym = "."

    def show(self):
        """Возвращает свой символ"""
        return self.__sym

class Area:
    """Матрица из клеток"""
    __x_size = 30
    __y_size = 30
    def __init__(self, ID):
        self.ID = ID
        self.square = [[Cage(x, y) for x in range(self.__x_size)] for y in range(self.__y_size)]

class Field:
    """Класс поля. Содержит список зон"""
    player_coords=(0,0)
    def __init__(self):
        """конструктор. Сначала есть единственная зона с ID = (0,0)"""
        self.squares=[Area((0,0))]

    def set_player(self, sym, x, y):
        """Метод установки игрока на клетку. деактивируется прошлая клетка, активируется новая."""
        area_id, cage_id = from_user_to_cage_coordinate((x, y))
        try:
            area_with_player = list(filter(lambda x: x.ID == area_id, self.squares))[0]
            if area_with_player.square[cage_id[1]][cage_id[0]].active:
                return 0
        except IndexError:
            pass
        area_id, cage_id = from_user_to_cage_coordinate(self.player_coords)
        area_with_player = list(filter(lambda x: x.ID == area_id, self.squares))[0]
        area_with_player.square[cage_id[1]][cage_id[0]].deactivate()
        self.player_coords = (x, y)
        area_id, cage_id = from_user_to_cage_coordinate(self.player_coords)
        try:
            area_with_player = list(filter(lambda x: x.ID == area_id, self.squares))[0]
            #if area_with_player.square[cage_id[1]][cage_id[0]].active:
            area_with_player.square[cage_id[1]][cage_id[0]].activate(sym)
            #else:
            #    return 0
        except IndexError:
            area_with_player = Area(area_id)
            self.squares.append(area_with_player)
            area_with_player.square[cage_id[1]][cage_id[0]].activate(sym)
    
    def set_enemy(self, sym, x, y):
        area_id, cage_id = from_user_to_cage_coordinate((x, y))
        try:
            area_with_enemy = list(filter(lambda x: x.ID == area_id, self.squares))[0]
            area_with_enemy.square[cage_id[1]][cage_id[0]].activate(sym, initiator = "enemy")
        except IndexError:
            area_with_enemy = Area(area_id)
            self.squares.append(area_with_enemy)
            area_with_enemy.square[cage_id[1]][cage_id[0]].activate(sym)

    def deactivate_by_non_player(self, sym, x, y):
        area_id, cage_id = from_user_to_cage_coordinate((x, y))
        area_with_player = list(filter(lambda x: x.ID == area_id, self.squares))[0]
        area_with_player.square[cage_id[1]][cage_id[0]].deactivate()

    def get_cage_by_coords(self, coords):
        """возвращает символ клетки по указанным координатам игрока"""
        area_id, cage_id = from_user_to_cage_coordinate(coords)
        try:
            area_with_player = list(filter(lambda x: x.ID == area_id, self.squares))[0]
        except IndexError:
            return " "
        return area_with_player.square[cage_id[1]][cage_id[0]].show()

if __name__ == "__main__":
    f = Field()
    f.show()