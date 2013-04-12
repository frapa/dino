import pyglet
from pyglet.gl import *
from .. import globe

class GuiGroup(pyglet.graphics.OrderedGroup):
    def __init__(self, scene, order, parent=None):
        super(GuiGroup, self).__init__(order, parent)
        self.scene = scene
        self.children = 0
    
    def getOrder(self, num):
        c = self.children
        self.children += num

        return c

    def set_state(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, globe.window.width, 0, globe.window.height, 0.0, 1.0)

    def unset_state(self):
        self.scene.move_scene_to(*self.scene.scene_pos)
