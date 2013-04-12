import pyglet
from ..entity.rect import Rect
from ..entity.entity import Entity
from button import Button
from .. import globe

TILE_SIZE = 48
BORDER = 15
SCROLL_WIDTH = 6
SCROLL_HEIGHT = 7
SIDEBAR_WIDTH = SCROLL_WIDTH * TILE_SIZE + BORDER * 2
SIDEBAR_COLOR = (100, 100, 100)
SCROLL_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (0, 0, 255)
SELECT_COLOR = (255, 0, 0)

class SideBar(object):
    def __init__(self, scene, batch):
        self.scene = scene
        self.batch = batch

        self.groups = {
            'background': pyglet.graphics.OrderedGroup(100),
            'middle': pyglet.graphics.OrderedGroup(101),
            'foreground': pyglet.graphics.OrderedGroup(102),
            'overlay1': pyglet.graphics.OrderedGroup(103),
            'overlay2': pyglet.graphics.OrderedGroup(104)
        }

        self.tiles = EntList()

        self.scroll = 0
        self.selected = None
        self.buttons = []

        self.init()

    def __del__(self):
        self.scroll_back.delete()
        self.background.delete()

        for tile in self.tiles:
            tile.delete()

    def init(self):
        w = globe.window.width
        h = globe.window.height
        sx = w - SIDEBAR_WIDTH
        es = SCROLL_HEIGHT * TILE_SIZE + BORDER

        # sidebar
        self.sidebar_rect = Rect(sx, 0, w - sx, h)

        self.background = self.batch.add(4, pyglet.gl.GL_QUADS, self.groups['background'],
            ('v2f', self.sidebar_rect.get_gl_points()),
            ('c3B', SIDEBAR_COLOR * 4)
        )

        # scroll
        self.scroll_rect = Rect(sx + BORDER, BORDER, SCROLL_WIDTH * TILE_SIZE, SCROLL_HEIGHT * TILE_SIZE)

        self.scroll_back = self.batch.add(4, pyglet.gl.GL_QUADS, self.groups['middle'],
            ('v2f', self.scroll_rect.grow(2).get_gl_points()), # 2 is the little border of scroll
            ('c3B', SCROLL_COLOR * 4)
        )

        for n, tile in enumerate(self.scene.tiles):
            y = n // SCROLL_WIDTH
            x = (n - y * SCROLL_WIDTH)
            
            ts = Entity(self.scene, tile[0], sx + BORDER + x * TILE_SIZE, BORDER + y * TILE_SIZE,
                batch=self.batch, group=self.groups['foreground'], world=False)

            self.tiles.append(ts)

        # buttons
        save_button = Button({"button": "resources/gui/button.png", "press": "resources/gui/button_pressed.png",
            "hover": "resources/gui/button_highlight.png"}, "Save",
            Rect(sx + BORDER, self.scroll_rect.bottom + BORDER, (SCROLL_WIDTH * TILE_SIZE - BORDER) / 2, 32),
            batch=self.batch, group=self.groups['middle'],
            callback=self.scene.save, font="Droid Sans")

        self.buttons.append(save_button)

        load_button = Button({"button": "resources/gui/button.png", "press": "resources/gui/button_pressed.png",
            "hover": "resources/gui/button_highlight.png"}, "Load",
            Rect(save_button.rect.right + BORDER, self.scroll_rect.bottom + BORDER, (SCROLL_WIDTH * TILE_SIZE - BORDER) / 2, 32),
            batch=self.batch, group=self.groups['middle'],
            callback=self.scene.load, font="Droid Sans")

        self.buttons.append(load_button)

    def push_buttons(self):
        for button in self.buttons:
            globe.window.push_handlers(button)

    def pop_buttons(self):
        for button in self.buttons:
            globe.window.pop_handlers()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.scroll_rect.collide_point(x, y):
            ix = (x - self.scroll_rect.left) // TILE_SIZE
            iy = (y - self.scroll_rect.top) // TILE_SIZE

            if ix + iy * SCROLL_WIDTH < len(self.tiles):
                if hasattr(self, 'highlight'):
                    self.highlight.delete()

                self.highlight = self.batch.add(4, pyglet.gl.GL_LINE_LOOP, self.groups['overlay1'],
                    ('v2f', self.tiles[ix + iy * SCROLL_WIDTH].rect.get_gl_points()),
                    ('c3B', HIGHLIGHT_COLOR * 4)
                )
            else:
                if hasattr(self, 'highlight'):
                    self.highlight.delete()
                    del self.highlight
        else:
            if hasattr(self, 'highlight'):
                self.highlight.delete()
                del self.highlight

    def on_mouse_press(self, x, y, button, modifiers):
        if self.sidebar_rect.collide_point(x, y):
            if self.scroll_rect.collide_point(x, y):
                ix = (x - self.scroll_rect.left) // TILE_SIZE
                iy = (y - self.scroll_rect.top) // TILE_SIZE
                
                if ix + iy * SCROLL_WIDTH < len(self.tiles):
                    if hasattr(self, 'select'):
                        self.select.delete()

                    self.select = self.batch.add(4, pyglet.gl.GL_LINE_LOOP, self.groups['overlay2'],
                        ('v2f', self.tiles[ix + iy * SCROLL_WIDTH].rect.get_gl_points()),
                        ('c3B', SELECT_COLOR * 4)
                    )

                    self.selected = ix + iy * SCROLL_WIDTH
