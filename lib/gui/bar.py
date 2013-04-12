import pyglet
from ..entity.entity import Entity

HEALTHY_COLOR = ((135, 220, 0), (110, 175, 0))
DAMAGED_COLOR = ((220, 150, 0), (220, 110, 0))
CRITICAL_COLOR = ((255, 80, 0), (200, 25, 0))
FULL_COLOR = ((10, 160, 255), (10, 110, 255))

HEALTH = (HEALTHY_COLOR, DAMAGED_COLOR, CRITICAL_COLOR)
ENERGY = (FULL_COLOR, FULL_COLOR, FULL_COLOR)

DAMAGED = 0.65
CRITICAL = 0.3

BORDER_COLOR = (0, 0, 0)
BACK_COLOR = ((35, 35, 35), (20, 20, 20))
OFFSET = 1
HEIGHT = 24

class Bar(object):
    def __init__(self, max_value, pos, max_length, value=None, batch=None, group=None, color=HEALTH):
        self.max_value = max_value
        if value == None:
            self.value = max_value
        else:
            self.value = value

        self.max_length = max_length
        self.x, self.y = pos
        self.color = color

        self.batch = batch
        self.group = group

        self.render()

    def animation(self, dt):
        if self.value > self.arrive_to:
            self.value -= 1
        elif self.value < self.arrive_to:
            self.value += 1
        else:
            pyglet.clock.unschedule(self.animation)

        self.render()

    def render(self):
        if hasattr(self, 'quad'):
            self.quad.delete()

        ratio = self.value / float(self.max_value)

        if ratio < CRITICAL:
            color = self.color[2]
        elif ratio < DAMAGED:
            color = self.color[1]
        else:
            color = self.color[0]

        level = self.group.getOrder(2)

        self.quad = self.batch.add(4, pyglet.gl.GL_QUADS, pyglet.graphics.OrderedGroup(level, self.group),
            ('v2f', (self.x, self.y, self.x + ratio * self.max_length, self.y,
                self.x + ratio * self.max_length, self.y + HEIGHT, self.x, self.y + HEIGHT)),
            ('c3B', color[1] * 2 + color[0] * 2)
        )

        self.border = self.batch.add(4, pyglet.gl.GL_LINE_LOOP, pyglet.graphics.OrderedGroup(level, self.group),
            ('v2f', (self.x - OFFSET + 1, self.y - OFFSET, self.x + OFFSET + self.max_length, self.y - OFFSET + 1,
                self.x + OFFSET + self.max_length, self.y + HEIGHT + OFFSET - 1, self.x - OFFSET, self.y + HEIGHT + OFFSET)),
            ('c3B', BORDER_COLOR * 4)
        )

        self.back = self.batch.add(4, pyglet.gl.GL_QUADS, pyglet.graphics.OrderedGroup(level - 1, self.group),
            ('v2f', (self.x - OFFSET, self.y - OFFSET, self.x + OFFSET + self.max_length, self.y - OFFSET,
                self.x + OFFSET + self.max_length, self.y + HEIGHT + OFFSET, self.x - OFFSET, self.y + HEIGHT + OFFSET)),
            ('c3B', BACK_COLOR[0] * 2 + BACK_COLOR[1] * 2)
        )

    def update(self, value):
        self.value = value
        self.render()

    def update_animation(self, value):
        self.arrive_to = value
        pyglet.clock.schedule(self.animation)
