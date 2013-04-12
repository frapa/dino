import pyglet
from ..entity.rect import Rect
from ..entity.entity import Entity

BORDER_SIZE = 4

class Button(object):
    def __init__(self, imgs, text, rect, callback, font=None, batch=None, group=None):
        """imgs can be an image path, an image or a dict with (some) of the following keys:
            button - normal button image
            press - pressed button
            hover - displayed when mouse is over
        """

        self.batch = batch
        self.group = group
        self.text = text
        self.rect = rect
        self.callback = callback
        self.images = {}

        if rect.height < 32:
            rect.height = 32

        if type(imgs) == dict:
            for key, img in imgs.items():
                if type(img) in (str, unicode):
                    img = pyglet.resource.image(img)
                    self.images[key] = self.create_image(img)

            self.sprite = pyglet.sprite.Sprite(self.images["button"],
                x=rect.left, y=rect.top,
                batch=self.batch, group=self.group)
        else:
            if type(imgs) in (str, unicode):
                imgs = pyglet.resource.image(imgs)
            
            self.image = self.create_image(imgs)

            self.sprite = pyglet.sprite.Sprite(self.image,
                x=rect.left, y=rect.top,
                batch=self.batch, group=self.group)

        self.label = pyglet.text.Label(text, font, 11, x=self.rect.center_x, y=self.rect.center_y,
            anchor_x='center', anchor_y='center',
            batch=batch, group=group)

    def __del__(self):
        self.label.delete()

    def create_image(self, img):
        rect = self.rect

        raw_img = img.get_image_data()
        pixel_data = raw_img.get_data('RGBA', 4 * raw_img.width)
        data_lines = [pixel_data[y * raw_img.width * 4:(y + 1) * raw_img.width * 4] for y in range(raw_img.height)]

        button_data = r''

        add = (rect.height - BORDER_SIZE * 2) - (raw_img.height - BORDER_SIZE * 2)
        add_every = None
        if add != 0:
            add_every = (rect.height - BORDER_SIZE * 2) // add
        
        for y in range(rect.height):
            for x in range(rect.width):
                if y <= BORDER_SIZE:
                    if x < BORDER_SIZE:
                        button_data += data_lines[y][x * 4:(x + 1) * 4]
                    elif x >= rect.width - BORDER_SIZE:
                        if (x - rect.width + 1) * 4 == 0:
                            button_data += data_lines[y][(x - rect.width) * 4:]
                        else:
                            button_data += data_lines[y][(x - rect.width) * 4:(x - rect.width + 1) * 4]
                    else:
                        button_data += data_lines[y][BORDER_SIZE * 4:(BORDER_SIZE + 1) * 4]
                elif y >= rect.height - BORDER_SIZE:
                    if x < BORDER_SIZE:
                        button_data += data_lines[y - rect.height][x * 4:(x + 1) * 4]
                    elif x >= rect.width - BORDER_SIZE:
                        if (x - rect.width + 1) * 4 == 0:
                            button_data += data_lines[y - rect.height][(x - rect.width) * 4:]
                        else:
                            button_data += data_lines[y - rect.height][(x - rect.width) * 4:(x - rect.width + 1) * 4]
                    else:
                        button_data += data_lines[y - rect.height][BORDER_SIZE * 4:(BORDER_SIZE + 1) * 4]
                else:
                    if add != 0:
                        real_y = y - (y - BORDER_SIZE) // add_every
                    else:
                        real_y = y

                    if x < BORDER_SIZE:
                        button_data += data_lines[real_y][x * 4:(x + 1) * 4]
                    elif x >= rect.width - BORDER_SIZE:
                        if (x - rect.width + 1) * 4 == 0:
                            button_data += data_lines[real_y][(x - rect.width) * 4:]
                        else:
                            button_data += data_lines[real_y][(x - rect.width) * 4:(x - rect.width + 1) * 4]
                    else:
                        button_data += data_lines[real_y][BORDER_SIZE * 4:(BORDER_SIZE + 1) * 4]


        button_img = pyglet.image.ImageData(rect.width, rect.height,
            'RGBA', button_data)
       
        return button_img

    def on_mouse_motion(self, x, y, dx, dy):
        if self.rect.collide_point(x, y):
            if self.images:
                try:
                    self.sprite.image = self.images["hover"]
                except KeyError:
                    pass
        elif self.images:
            self.sprite.image = self.images["button"]
        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.rect.collide_point(x, y):
            self.callback()
            
            if self.images:
                try:
                    self.sprite.image = self.images["press"]
                except KeyError:
                    pass

            return True

    def on_mouse_released(self, x, y, button, modifiers):
        if self.images:
            self.sprite.image = self.images["button"]
