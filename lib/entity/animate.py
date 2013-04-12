import os
import json
import pyglet
import entity
from .. import globe as globe

INTERVAL = 0.1
no_loop = ('_fight',)

# Represents an animated thing. It extends the basic entity features, and allows
# to easily load animations for static things.
class Animated(entity.Entity):
    def __init__(self, scene, img, frames, rect, interval=INTERVAL, batch=None, group=None, add=True):
        if type(img) in (str, unicode):
            img = pyglet.resource.image(img)

        if frames == 1:
            super(Animable, self).__init__(scene, img, batch=batch, group=group, rect=rect, add=add)
        else:
            seq = pyglet.image.ImageGrid(img, 1, frames)
            ani = pyglet.image.Animation.from_image_sequence(seq, interval)

            super(Animated, self).__init__(scene, ani, batch=batch, group=group, rect=rect, add=add)

# Represents an animable entity. It loads all animations from a directory.
# It also loads a file which tells the animation timings.
class Animable(entity.Entity):
    def __init__(self, scene, name, rect, batch=None, group=None, add=True):
        self.name = name

        # load all stuff from name directory
        path = os.path.join(globe.path, 'resources', 'sprites', name)
        
        with open(os.path.join(path, "timings.json")) as f:
            timings = json.load(f)

            self.images = {}
            self.sequencies = {}
            self.animations = {}

            self.images[name] = pyglet.resource.image(os.path.join('sprites', name, name + '.png'))
            width = self.images[name].width
            height = self.images[name].height

            for filename in os.listdir(path):
                only_name, ext = os.path.splitext(filename)

                if ext == '.png':

                    if only_name != name:
                        img = pyglet.resource.image(os.path.join('sprites', name, filename))

                        if img.width != width:
                            try:
                                self.load_ani(only_name, img, img.width / width, timings[only_name])
                            except:
                                print 'Tried to load animation of the wrong size'
                        else:
                            self.images[only_name] = img

            super(Animable, self).__init__(scene, self.images[name], batch=batch, group=group, rect=rect, add=add)
    
    def load_ani(self, name, img, frames, interval):
        seq = pyglet.image.ImageGrid(img, 1, frames)
        ani = pyglet.image.Animation.from_image_sequence(seq, interval,
                any([name.find(s) == -1 for s in no_loop]))

        self.sequencies[name] = seq
        self.animations[name] = ani
