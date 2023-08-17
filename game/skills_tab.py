class Skills_tab:
    max_attack = 100
    max_health = 100
    max_speed = 0
    def __init__(self, player):
        self.points = 0
        self.attack_points = 0
        self.health_points = 0
        self.speed_points = 0
        self.pl = player
    
    def increase_skill(self, skill):
        if not self.points:
            return
        match skill:
            case "attack":
                if self.attack_points<self.max_attack:
                    self.attack_points+=1
                    self.pl.increase_param("attack", 0.01*self.attack_points)
            case "health":
                if self.health_points<self.max_health:
                    self.health_points+=1
                    self.pl.increase_param("health", 10*self.health_points)
            case "speed":
                if self.speed_points<self.max_speed:
                    self.speed_points+=1
                    self.pl.increase_param("speed", 1)
            case "regeneration":
                self.pl.regeneration()
        self.points-=1
    def get_tab(self,size_x, size_y):
        lines = 6
        text = f"+{'='*(size_x-3)}+\n"
        text += f"|{' '*(size_x-3)}|\n"
        text += f"| Skill points: {self.points}{' ' * (size_x - 18 - len(str(self.points)))}|\n"
        text += f"|{' '*(size_x-3)}|\n"
        text += f"| 1) Healing:{' ' * (size_x - 15)}|\n"
        text += f"|{' '*(size_x-3)}|\n"
        if self.health_points<self.max_health:
            text += f"| 2) Health --- {self.health_points}{' '*(size_x - 18 - len(str(self.health_points)))}|\n"
            text += f"|{' '*(size_x-3)}|\n"
            lines+=2
        if self.attack_points<self.max_attack:
            text += f"| 3) Attack --- {self.attack_points}{' '*(size_x - 18 - len(str(self.attack_points)))}|\n"
            text += f"|{' '*(size_x-3)}|\n"
            lines+=2
        if self.speed_points<self.max_speed:
            text += f"| 4) Speed --- {self.speed_points}{' '*(size_x - 18)}|\n"
            lines+=1
        if lines<size_y:
            if size_y-lines > 1:
                text+= f"|{' '*(size_x-3)}|\n"*(size_y-lines-1)
            text+= f"+{'='*(size_x-3)}+"
        else:
            return "RESIZE TERMINAL WINDOW!!!"
        return text
        
