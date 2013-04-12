import os
import pyglet
import scene
from ..entity.rect import Rect
from .. import globe
from ..gui.list import ListWidget 

BACKGROUND_COLOR = (0.39, 0.39, 0.39, 1) # about 100/255
BORDER = 15

class FileScene(scene.Scene):
    def __init__(self, parent):
        super(FileScene, self).__init__(parent)

        pyglet.gl.glClearColor(*BACKGROUND_COLOR)

        self.list_widget = ListWidget(Rect(BORDER, BORDER, globe.window.width - 2 * BORDER, globe.window.height - 2 * BORDER), 2,
            batch=self.batch, group=pyglet.graphics.OrderedGroup(1), font='Droid Sans', callback=self.enter)

        self.update('~')

    def start(self):
        self.parent.push_handlers(self.list_widget)

    def update(self, path):
        self.path = os.path.expanduser(path)

        self.list_widget.clear()
        self.list_widget.set_cols(('File', 'Size'))

        for f in os.listdir(self.path):
            if f[0] != '.':
                stat = os.stat(os.path.join(self.path, f))
                self.list_widget.add_element(f, str(stat.st_size / 1024) + ' Kb')

    def enter(self, element):
        path = os.path.join(self.path, element['cols'][0])

        if os.path.isdir(path):
            self.update(path)

    def end(self):
        self.parent.pop_handlers()
