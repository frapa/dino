# Despite the name, this class keeps all the information
# about a character health, armor, power-ups, abilities,
# and other stuff useful for game logic
class Armor(object):
    def __init__(self, health, hit_points, energy=100, armor=0):
        self.health = health
        self.hit_points = hit_points
        self.energy = energy
        self.armor = armor

        self.aura = 'basic'

        # normal attack
        self.attack_range = 50
        self.attack_energy = 5

    def attack(self, other):
        other.health -= self.hit_points - self.hit_points * other.armor
