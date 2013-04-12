import pyglet
from ..entity.animate import Animated, INTERVAL

class Particle(Animated):
    def __init__(self, scene, img, frames, rect, interval=INTERVAL, batch=None, group=None, timeout=None):
        super(Particle, self).__init__(scene, img, frames, rect, interval, batch, group)

        if timeout == None:
            pyglet.clock.schedule_once(self.remove, INTERVAL * frames)
        else:
            pyglet.clock.schedule_once(self.remove, timeout)

    def remove(self, dt):
        self.scene.entities.remove(self)
