import os
from math import sqrt
import pyglet
import entity
import animate
from lib.entity.rect import Rect
from lib.effects.particle import Particle
from lib.armor.armor import Armor
from .. import globe as globe

WALK_SPEED = 250
JUMP_SPEED = 750
JUMPY_ATTACK_SPEED = 800

class Char(animate.Animable):
    def __init__(self, scene, name, rect, batch=None, group=None, add=True, health=100):
        super(Char, self).__init__(scene, name, batch=batch, group=group, rect=rect, add=add)

        self.speed = WALK_SPEED

        # is char on the ground?
        self.on_ground = False
        # is char pushing on a wall?
        self.on_wall = False
        self.fighting = False
        self.would_walk = 0
        self.just_damaged = False
        self.invulnerable = False

        self.armor = Armor(health=health, hit_points=10)
    
    def walk_left(self, speed=None):
        if speed == None:
            speed = self.speed

        if not self.fighting:
            self.velocity[0] = -speed

            if self.on_ground:
                self.sprite.image = self.animations[self.name + '_walk_back']
            else:
                self.sprite.image = self.images[self.name + '_jump_left']
        else:
            self.would_walk = -1

    def walk_right(self, speed=None):
        if speed == None:
            speed = self.speed

        if not self.fighting:
            self.velocity[0] = speed

            if self.on_ground:
                self.sprite.image = self.animations[self.name + '_walk']
            else:
                self.sprite.image = self.images[self.name + '_jump_right']
        else:
            self.would_walk = 1

    def stop_walking(self):
        self.velocity[0] = 0
        self.would_walk = 0

        self.sprite.image = self.images[self.name]

    def stop_walking_left(self):
        if self.velocity[0] in (-self.speed, 0):
            self.velocity[0] = 0
            self.would_walk = 0

            if self.on_ground and not self.fighting:
                self.sprite.image = self.images[self.name + '_back']

    def stop_walking_right(self):
        if self.velocity[0] in (self.speed, 0):
            self.velocity[0] = 0
            self.would_walk = 0

            if self.on_ground and not self.fighting:
                self.sprite.image = self.images[self.name]

    def stop(self):
        self.on_wall = True

        if self.on_ground and self.velocity[1] == 0:
            if self.velocity[0] > 0:
                self.sprite.image = self.images[self.name + "_stop_right"]
            else:
                self.sprite.image = self.images[self.name + "_stop_left"]

    def jump(self):
        if not self.fighting and self.on_ground:
            self.velocity[1] = JUMP_SPEED

            self.on_ground = False

            if self.velocity[0] > 0:
                self.sprite.image = self.images[self.name + "_jump_right"]
            elif self.velocity[0] < 0:
                self.sprite.image = self.images[self.name + "_jump_left"]
            else:
                if self.sprite.image == self.images[self.name]:
                    self.sprite.image = self.images[self.name + "_jump_right"]
                else:
                    self.sprite.image = self.images[self.name + "_jump_left"]

    def fight(self):
        if not self.fighting:
            if self.on_ground:
                self.fighting = True
                self.would_walk = self.velocity[0] / self.speed
                self.velocity[0] = 0

                if self.would_walk < 0:
                    self.sprite.image = self.animations[self.name + "_fight_back"]
                else:
                    self.sprite.image = self.animations[self.name + "_fight"]

                self.sprite.set_handler('on_animation_end', self.animation_end)

                dt = self.sprite.image.get_duration()
                pyglet.clock.schedule_once(self.aura, dt)

                self.become_invulnerable(0.5)

                # check if there are enemies nearby
                for other in self.scene.movable:
                    if other != self and self.rect.distance(other.rect) < self.armor.attack_range:
                        self.attack(other)
            #elif abs(self.velocity[1]) < 0.8*JUMP_SPEED:
            #    self.fighting = True
            #    self.would_walk = self.velocity[0] / self.speed
            #    self.velocity = [0, 0]

            #    pyglet.clock.schedule_once(self.jumpy_attack, 0.25)
            #    self.enable_gravity(0)

            #    self.invulnerable = True
            #    pyglet.clock.schedule_once(self.end_attack, 0.5)

            #    if self.would_walk < 0:
            #        self.sprite.image = self.images[self.name + '_jumpy_back']
            #    else:
            #        self.sprite.image = self.images[self.name + '_jumpy']

    def aura(self, dt):
        # this draws the nice attack effect
        aura = Particle(self.scene, 'objects/aura/{}.png'.format(self.armor.aura), 3,
                rect=Rect(self.rect.left - 8, self.rect.top, 64, 64),
                batch=self.scene.batch,
                group=self.scene.groups['tiles'])

    def animation_end(self):
        if self.fighting:
            self.sprite.image = self.images[self.name]

            self.fighting = False

            if self.would_walk == -1:
                self.walk_left()
            elif self.would_walk == 1:
                self.walk_right()

    def hit_the_ground(self):
        self.velocity[1] = 0

        if not self.on_ground:
            self.on_ground = True

            if self.fighting:
                self.fighting = False

            if self.velocity[0] > 0 or self.would_walk > 0:
                self.walk_right()
            elif self.velocity[0] < 0 or self.would_walk < 0:
                self.walk_left()
            else:
                if self.sprite.image == self.images[self.name + '_jump_right']:
                    self.sprite.image = self.images[self.name]
                else:
                    self.sprite.image = self.images[self.name + "_back"]

    def hit_the_ceiling(self):
        self.velocity[1] = 0

    def attack(self, other):
        self.become_invulnerable(0.5)
        self.damage(other)

    def become_invulnerable(self, time):
        self.invulnerable = True
        pyglet.clock.schedule_once(self.end_invulnerable, time)

    def end_invulnerable(self, dt):
        self.invulnerable = False

    def jumpy_attack(self, dt):
        self.velocity = [0, -JUMPY_ATTACK_SPEED]
        self.enable_gravity()

    def damage(self, other):
        self.armor.attack(other.armor)

        if other.armor.health <= 0:
            self.scene.movable.remove(other)
            self.scene.entities.remove(other)
        elif self.scene.char == other:
            other.just_damaged = True

            pyglet.clock.schedule_once(other.end_damaged, 1.2)
            other.sprite.opacity = 180

            self.scene.gui["health_bar"].update_animation(other.armor.health)

    def end_damaged(self, dt):
        self.sprite.opacity = 255
        self.just_damaged = False
