import pyglet
from rect import Rect
from .. import vector

GRAVITY = -1500

class Entity(object):
    def __init__(self, scene, img=None, x=0, y=0, batch=None, group=None, rect=None, world=True, add=True):
        self.scene = scene
        if add:
            self.scene.entities.append(self)

        self.batch = batch
        self.group = group
        self.world = world #???

        self.offset = (0, 0)
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

        image = None

        # string of image to be loaded
        if type(img) in (str, unicode):
            image = pyglet.resource.image(img)
            self.type = 'sprite'
        # not image but block
        elif type(img) == dict:
            self.type = 'block'
            vertices = img["vertices"]
            color = []
            
            # vertices can be passed it rect format (x, y, width, height)
            # or normal format (x1, y1, x2, x2, ...., x4, y4)
            if len(vertices) == 4:
                x, y, w, h = vertices
                vertices = (x, y, x + w, y, x + w, y + h, x, y + h)

            if len(img["color"]) == 3:
                color = img["color"] * 4
            else:
                color = img["color"]

            self.vertices = self.batch.add(4, pyglet.gl.GL_QUADS, self.group,
                ('v2f', vertices),
                ('c3B', color)
            )

            if rect == None:
                # vertices can be passed it rect format (x, y, width, height)
                # or normal format (x1, y1, x2, x2, ...., x4, y4)
                if len(img["vertices"]) == 4:
                    self.rect = Rect(*img["vertices"])
                else:
                    self.rect = Rect(vertices[0], vertices[1], vertices[2] - vertices[1],
                        vertices[5] - vertices[1])
            else:
                self.rect = rect
        # does not show anything, only for other things (collisions)
        elif img == None:
            self.type = 'none'
            self.rect = rect
        # image already given
        else:
            self.type = 'sprite'
            image = img

        # if sprite, create sprite, and rect
        if self.type == 'sprite':
            # create rect from sprite
            if rect == None:
                self.sprite = pyglet.sprite.Sprite(image,
                    x=x, y=y, batch=batch, group=group)

                self.rect = Rect(x, y, image.width, image.height)
            # custom rect
            else:
                self.sprite = pyglet.sprite.Sprite(image,
                    x=rect.left, y=rect.top, batch=batch, group=group)

                self.rect = rect

    def delete(self):
        self.sprite.delete()

    def enable_gravity(self, g=GRAVITY):
        self.acceleration[1] = g

    def step_x(self, dt):
        self.velocity[0] += self.acceleration[0] * dt

        self.move(self.velocity[0] * dt, 0)
        
    def step_y(self, dt):
        self.velocity[1] += self.acceleration[1] * dt

        self.move(0, self.velocity[1] * dt)

    # decopule sprite and rect!
    def set_offset(self, x, y):
        self.offset = (x, y)
        self.sprite.set_position(self.rect.left + self.offset[0],
                self.rect.top + self.offset[1])

    def move(self, x, y):
        self.rect.move(x, y)
        self.sprite.set_position(self.rect.left + self.offset[0],
                self.rect.top + self.offset[1])

#class EntList(object):
#    def __init__(self):
#        self.entities = []
#        self.imp_ent = {}
#
#    def append(self, x):
#        self.entities.append(x)
#
#    def remove(self, x):
#        if x in self.entities:
#            self.entities.remove(x)
#            x.delete() 
#
#    def delete(self, key):
#        self.imp_ent[key].delete()
#
#        self.entities.remove(self.imp_ent[key])
#        del self.imp_ent[key]
#
#    def __iter__(self):
#        return self.entities.__iter__()
#
#    def __len__(self):
#        return len(self.entities)
#
#    def __contains__(self, x):
#        return x in self.entities
#
#    def __getitem__(self, key):
#        if type(key) == int:
#            return self.entities[key]
#        else:
#            return self.imp_ent[key]
#
#    def __setitem__(self, key, value):
#        self.imp_ent[key] = value
#
#        if not (value in self.entities):
#            self.entities.append(value)
#
#    def __delitem__(self, key):
#        self.entities.remove(self.imp_ent[key])
#        del self.imp_ent
#
#    def __repr__(self):
#        return repr(self.entities)
