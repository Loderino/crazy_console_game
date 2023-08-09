import random
class Weapon:
    def __init__(self, name, status, anim, length):
        epitets = [" огня", " смерти", " крови", " холодных земель", " луны"]
        random.shuffle(epitets)
        self.name = name + epitets[0]
        self.status = status
        self.anim = anim
        self.length = length
        match status:
            case "D":
                self.attack = random.randint(1, 10)
            case "C":
                self.attack = random.randint(10, 25)
            case "B":
                self.attack = random.randint(25, 50)
            case "A":
                self.attack = random.randint(50, 100)
            case "S":
                self.attack = random.randint(100, 250)
            case "SSS":
                self.attack = random.randint(500, 1000)
    
    def __str__(self):
        return f"{self.name} | радиус атаки {self.length} | урон {self.attack} | класс {self.status}"

    def get_information(self):
        return (self.attack, self.length, self.anim)