import pyglet
import char

class BaseEnemy(char.Char):
    def __init__(self, scene, name, rect, batch=None, group=None, add=True, health=10):
        super(BaseEnemy, self).__init__(scene, name, batch=batch, group=group, rect=rect, add=add, health=health)

        if add:
            self.scene.movable.append(self)

        self.speed = 100

        self.invert = False

        self.walk_left()

    def step_x(self, dt):
        if self.invert:
            if self.velocity[0] > 0:
                self.walk_left()
            else:
                self.walk_right()

            self.invert = False

        self.velocity[0] += self.acceleration[0] * dt

        self.move(self.velocity[0] * dt, 0)

        for other in self.scene.collision:
            if other != self and self.rect.collide(other.rect):
                self.invert = True

    def touch(self, entity):
        if not entity.just_damaged or entity.invulnerable:
            self.attack(entity)
