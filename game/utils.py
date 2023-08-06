def from_user_to_cage_coordinate(player_coordinates):
    """Координаты для игрока и координаты на поле разные. Эта функция переводит координаты игрока в координаты поля"""
    player_x = player_coordinates[0]
    player_y = player_coordinates[1]
    area_x = 0
    area_y = 0
    cage_x = 0
    cage_y = 0
    if player_x>0:
        if player_x<=14:
            area_x = 0
            cage_x = 15+player_x
        else:
            player_x-=15
            area_x = player_x//30+1
            cage_x = player_x%30

    elif player_x<0:
        if player_x>=-15:
            area_x = 0
            cage_x = 15+player_x
        else:
            player_x+=15
            area_x = player_x//30
            cage_x = player_x%30
    else:
        area_x = 0
        cage_x = 15

    if player_y>0:
        if player_y<=14:
            area_y = 0
            cage_y = 15+player_y
        else:
            player_y-=15
            area_y = player_y//30+1
            cage_y = player_y%30

    elif player_y<0:
        if player_y>=-15:
            area_y = 0
            cage_y = 15+player_y
        else:
            player_y+=15
            area_y = player_y//30
            cage_y = player_y%30
    else:
        area_y = 0
        cage_y = 15
    return ((area_x, area_y), (cage_x, cage_y))

if __name__ == "__main__":
    for i in range(0, -100, -1):
        print(i, "-", from_user_to_cage_coordinate((i, i)))

