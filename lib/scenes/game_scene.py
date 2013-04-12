import random
import os

import pyglet
from pyglet.window import key
from pyglet.gl import *

import scene
from load_map import load_map
from ..entity.rect import Rect
from ..entity.entity import Entity
from ..entity.animate import Animated
from ..entity.char import Char
from ..entity.enemy import BaseEnemy
from ..effects.particle import Particle
from ..gui.bar import Bar, ENERGY
from ..gui.group import GuiGroup
from .. import globe

class GameScene(scene.Scene):
    def __init__(self, parent):
        super(GameScene, self).__init__(parent)

        # used for animations
        #self.sequencies = {}
        #self.animations = {}

        # special entities
        self.movable = [] # those that can move
        self.collision = [] # those that collide
        self.dangerous = [] # those that hurt
        #self.differential = [] # those that moves differentely from foreground

        # player char
        self.char = None

        # groups for rendering everything in the right order
        self.groups = {
            'sky': pyglet.graphics.OrderedGroup(0),
            'background': pyglet.graphics.OrderedGroup(10000),
            'ground': pyglet.graphics.OrderedGroup(15000),
            'environment': pyglet.graphics.OrderedGroup(20000),
            'tiles': pyglet.graphics.OrderedGroup(30000),
            'chars': pyglet.graphics.OrderedGroup(40000),
            'foreground': pyglet.graphics.OrderedGroup(50000),
            'gui': GuiGroup(self, 60000)
        }

        self.gui = {}

        # camera position
        self.camera_pos = [0, 0]

#    def load_ani(self, filename, frames, interval):
#        name = os.path.splitext(os.path.split(filename)[1])[0]
#
#        img = pyglet.resource.image(filename)
#        seq = pyglet.image.ImageGrid(img, 1, frames)
#        ani =  pyglet.image.Animation.from_image_sequence(seq, interval)
#
#        self.sequencies[name] = seq
#        self.animations[name] = ani

    def load_map(self, map_file):
        load_map(self, map_file)

    def move_scene(self, dx, dy):
        self.move_scene_to(self.scene_pos[0] + dx, self.scene_pos[1] + dy)

    def move_scene_to(self, x, y):
        self.scene_pos = [x, y]

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        spx, spy = map(int, self.scene_pos)
        glOrtho(spx, spx + globe.window.width, spy, spy + globe.window.height, 0.0, 1.0)

        # adjust sky!
        if hasattr(self, 'sky'):
            self.sky.vertices = [spx, spy, spx + globe.window.width, spy,
                spx + globe.window.width, spy + globe.window.height, spx, spy + globe.window.height]

        # implement self.differential entities

    def start(self):
        pyglet.clock.schedule_once(self.start_char, 0.5)
        pyglet.clock.schedule_interval(self.step, 0.04)

    def start_char(self, dt):
        self.char.sprite.batch = self.batch

        self.movable.append(self.char)

        puff_img = pyglet.resource.image('objects/puff.png')

#        for a in range(3):
#            puff = Particle(self, puff_img, 5, 
#                rect=Rect(self.char.rect.left + random.randint(-24, 24),
#                    self.char.rect.top + random.randint(-24, 24),
#                    puff_img.width, puff_img.height), batch=self.batch,
#                group=self.groups.values()[1 + a])

        self.entities.append(self.char)

    # physics simulation goes here
    def step(self, dt):
        # update position and velocity along x axis
        for entity in self.movable:
            entity.step_x(dt)

        # collision along x
        for entity in self.movable:
            for other in self.collision:
                if entity != other and entity.rect.collide(other.rect):
                    penetration = entity.rect.get_penetration_x(other.rect)
                    
                    if entity.velocity[0] != 0:
                        entity.move(-(penetration + 1) * entity.velocity[0] / abs(entity.velocity[0]), 0)

                    entity.stop()
                elif isinstance(entity, Char):
                    entity.on_wall = False

        # update position and velocity
        for entity in self.movable:
            entity.step_y(dt)

        # collision along y
        for entity in self.movable:
            for other in self.collision:
                if entity != other and entity.rect.collide(other.rect):
                    penetration = entity.rect.get_penetration_y(other.rect)
                    
                    if entity.velocity[1] != 0:
                        entity.move(0, -(penetration + 1) * entity.velocity[1] / abs(entity.velocity[1]))

                    if entity.velocity[1] < 0:
                        entity.hit_the_ground()
                    else:
                        entity.hit_the_ceiling()
                elif isinstance(entity, Char):
                    entity.on_ground = False

        # collision with other movables
        for other in self.movable:
            if other != self.char and self.char.rect.collide(other.rect):
                other.touch(self.char)

        cx = self.char.rect.center_x - globe.window.width / 2
        cy = self.char.rect.center_y - globe.window.height / 2

        self.move_scene_to(cx, cy)

    def on_key_press(self, symbol, modifiers):
        if self.char:
            if symbol == key.LEFT:
                self.char.walk_left()
            elif symbol == key.RIGHT:
                self.char.walk_right()
            elif symbol == key.SPACE:
                self.char.jump()
            elif symbol == key.X:
                self.char.fight()

    def on_key_release(self, symbol, modifiers):
        if self.char:
            if symbol == key.LEFT:
                self.char.stop_walking_left()
            if symbol == key.RIGHT:
                self.char.stop_walking_right()
