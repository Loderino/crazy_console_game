# crazy_console_game
I am crazy man, so a want to create a console rpg game

# В ПЛАНАХ #
- игрок - символ @ управляется кнопками wasd ✅
- Перемещение происходит по карте, которая каким-то образом будет генерироваться ✅ 
- У игрока будут параметры, определяющие скорость, атаку и т.д. ❌
- Будут враги. ❌
- Будет оружие. ❌
- Креативный директор постарается придумать Лор. ❌
- В планах есть ввод боссов, но это не скоро. ❌
- Да поможет нам Бог! ✅

# ЗАПУСК #

```bash
. script1.sh
sh start_game.sh
```

# Игровой процесс #

- Игрок - @ на карте
- Перемещение с помощью кнопок WASD
- Карта состоит из точек. Карта будет расширяться при пересечении границы точек.

# Служебная информация #

Система координат для игрока и на поле - разные.
Игрок изначально находится по координатам (0,0)
Эта точка соответствует области(0,0)(15, 15) - зона (0, 0), клетка (15, 15)
