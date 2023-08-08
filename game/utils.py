from game import field

def from_user_to_cage_coordinate(player_coordinates):
    """Координаты для игрока и координаты на поле разные. Эта функция переводит координаты игрока в координаты поля"""
    player_x = player_coordinates[0]
    player_y = player_coordinates[1]
    area_x = 0
    area_y = 0
    cage_x = 0
    cage_y = 0
    area_size_x, area_size_y = field.Area.x_size, field.Area.y_size
    if player_x>0:
        if player_x<=area_size_x//2-1:
            area_x = 0
            cage_x = area_size_x//2+player_x
        else:
            player_x-=area_size_x//2
            area_x = player_x//area_size_x+1
            cage_x = player_x%area_size_x

    elif player_x<0:
        if player_x>=-area_size_x//2:
            area_x = 0
            cage_x = area_size_x//2+player_x
        else:
            player_x+=area_size_x//2
            area_x = player_x//area_size_x
            cage_x = player_x%area_size_x
    else:
        area_x = 0
        cage_x = area_size_x//2

    if player_y>0:
        if player_y<=area_size_y//2-1:
            area_y = 0
            cage_y = area_size_y//2+player_y
        else:
            player_y-=area_size_y//2
            area_y = player_y//area_size_y+1
            cage_y = player_y%area_size_y

    elif player_y<0:
        if player_y>=-area_size_y//2:
            area_y = 0
            cage_y = area_size_y//2+player_y
        else:
            player_y+=area_size_y//2
            area_y = player_y//area_size_y
            cage_y = player_y%area_size_y
    else:
        area_y = 0
        cage_y = area_size_y//2
    return ((area_x, area_y), (cage_x, cage_y))

if __name__ == "__main__":
    for i in range(0, -100, -1):
        print(i, "-", from_user_to_cage_coordinate((i, i)))

