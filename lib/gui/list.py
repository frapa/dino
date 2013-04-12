import pyglet
from pyglet.window import key
from ..entity.rect import Rect
from ..entity.entity import Entity

BACKGROUND_COLOR = (50, 50, 50)
HEADER_COLOR = (70, 70, 70)
SELECTION_COLOR = (190, 120, 0)
BORDER = 5

class ListWidget(object):
    def __init__(self, rect, cols=1, font=None, batch=None, group=None, callback=lambda: None):
        self.batch = batch
        self.rect = rect
        self.font = font
        self.cols = cols
        self.callback = callback

        self.group = group
        self.selection_group = pyglet.graphics.OrderedGroup(2)
        self.text_group = pyglet.graphics.OrderedGroup(3)

        font = pyglet.font.load(self.font, 11)
        self.text_size = font.ascent - font.descent
        self.element_size = self.text_size + 2 * BORDER

        self.col_size = (self.rect.width / self.cols,) * self.cols

        self.elements = []

        self.batch.add(4, pyglet.gl.GL_QUADS, self.group,
            ('v2f', self.rect.get_gl_points()),
            ('c3B', BACKGROUND_COLOR * 4)
        )

    def set_cols(self, headers, sizes=None):
        if sizes:
            self.col_size = sizes

        self.add_element(*headers, pos=0)

        self.batch.add(4, pyglet.gl.GL_QUADS, self.selection_group,
            ('v2f', (self.rect.left, self.rect.bottom, self.rect.right, self.rect.bottom,
                self.rect.right, self.rect.bottom - BORDER - self.element_size,
                self.rect.left, self.rect.bottom - BORDER - self.element_size)),
            ('c3B', HEADER_COLOR * 4)
        )

    def add_element(self, *args, **kwargs):
        num = len(self.elements)

        pos = 0
        labels = []
        for n, text in enumerate(args):
            label = pyglet.text.Label(text, self.font, 11,
                x=self.rect.left + 2 * BORDER + pos, y=self.rect.bottom - 2 * BORDER - num * self.element_size,
                anchor_y='top', batch=self.batch, group=self.text_group)
            
            pos += self.col_size[n]
            labels.append(label)

        if 'pos' in kwargs:
            self.elements.insert(kwargs['pos'], {'num': num, 'cols': args, 'labels': labels})
        else:
            self.elements.append({'num': num, 'cols': args, 'labels': labels})

    def clear(self):
        for element in self.elements:
            for label in element['labels']:
                label.delete()

        self.elements = []

        if hasattr(self, 'selection'):
            self.selection.delete()
            del self.selection

        if hasattr(self, 'selected'):
            del self.selected

    def set_selection(self):
        if hasattr(self, 'selection'):
            self.selection.delete()

        self.selection = self.batch.add(4, pyglet.gl.GL_QUADS, self.selection_group,
            ('v2f', (self.rect.left, self.rect.bottom - BORDER - self.selected * self.element_size,
                self.rect.right, self.rect.bottom - BORDER - self.selected * self.element_size,
                self.rect.right, self.rect.bottom - BORDER - (self.selected + 1) * self.element_size,
                self.rect.left, self.rect.bottom - BORDER - (self.selected + 1) * self.element_size)),
            ('c3B', SELECTION_COLOR * 4)
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if not hasattr(self, 'selected'):
                self.selected = len(self.elements)

            if self.selected > 1:
                self.selected -= 1
                self.set_selection()
        elif symbol == key.DOWN:
            if not hasattr(self, 'selected'):
                self.selected = 0

            if self.selected < len(self.elements) - 1:
                self.selected += 1
                self.set_selection()
        elif symbol == key.ENTER:
            if hasattr(self, 'selected'):
                self.callback(self.elements[self.selected])
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.rect.collide_point(x, y):
            iy = (self.rect.bottom - BORDER - y) / self.element_size

            if 0 < iy < len(self.elements):
                self.selected = iy

                self.set_selection()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.rect.collide_point(x, y):
            iy = (self.rect.bottom - BORDER - y) / self.element_size

            if 0 < iy < len(self.elements):
                self.callback(self.elements[iy])
