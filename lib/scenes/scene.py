import pyglet
from ..entity.entity import Entity

class Scene(object):
    def __init__(self, parent):
        self.parent = parent

        self.batch = pyglet.graphics.Batch()
        self.groups = {}

        self.entities = []
        self.entity_dict = {}

    def change_scene(self, new_scene):
        self.parent.scene.end()
        self.parent.scene = new_scene

        # events
        self.parent.pop_handlers()
        self.parent.push_handlers(new_scene)

        new_scene.start()

    def start(self):
        pass

    def end(self):
        pass

    def on_draw(self):
        self.parent.clear()

        self.batch.draw()
