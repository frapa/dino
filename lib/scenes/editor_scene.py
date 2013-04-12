import random
import os

import pyglet
from pyglet.window import key

import scene
import game_scene
import file_scene
from ..entity.rect import Rect
from ..entity.entity import Entity
from ..gui.sidebar import SideBar
from .. import globe

TILE_SIZE = 48
SCROLL_SPEED = 40
GRID_COLOR = (80, 80, 80)
PATH = 'resources/tiles'

class EditorScene(game_scene.GameScene):
    def __init__(self, parent):
        super(EditorScene, self).__init__(parent)

        self.tiles = []
        for f in os.listdir(PATH):
            if os.path.isfile(os.path.join(PATH, f)):
                name, ext = os.path.splitext(f)
                if name == 'x':
                    self.tiles.insert(0, (pyglet.resource.image(os.path.join(PATH, f)), name))
                else:
                    self.tiles.append((pyglet.resource.image(os.path.join(PATH, f)), name))

        if globe.map_path and os.path.exists(globe.map_path):
            self.load_map(globe.map_path)
        

        #self.init()
        #self.init_sidebar()
        self.just_now = True

    def init(self):
        if hasattr(self, 'grid'):
            self.grid.delete()

        nw = globe.window.width / TILE_SIZE + 1
        nh = globe.window.height / TILE_SIZE + 1

        sx = self.scene_pos[0] / TILE_SIZE
        sy = self.scene_pos[1] / TILE_SIZE

        vertices = []
        colors = []
        for i in range(sx, sx + nw):
            x = i * TILE_SIZE - self.scene_pos[0]

            vertices.extend((x, 0, x, globe.window.height))
            colors.extend(GRID_COLOR * 2)

        for j in range(sy, sy + nh):
            y = j * TILE_SIZE - self.scene_pos[1]

            vertices.extend((0, y, globe.window.width, y))
            colors.extend(GRID_COLOR * 2)

        self.grid = self.batch.add((nw + nh) * 2, pyglet.gl.GL_LINES, self.groups['foreground'],
            ('v2f', vertices),
            ('c3B', colors)
        )
    
    def init_sidebar(self):
        if hasattr(self, 'sidebar'):
            self.sidebar.pop_buttons()
            globe.window.pop_handlers()

        self.sidebar = SideBar(self, self.batch)

    def start(self):
        globe.window.push_handlers(self.sidebar)
        self.sidebar.push_buttons()

    def on_resize(self, width, height):
        if not self.just_now:
            self.init()
            self.init_sidebar()
            self.start()
        else:
            self.just_now = False

    def load_map(self, map_file):
        load_map(self, map_file, load_chars=False)

    def save(self):
        self.write(globe.map_path)
    
    def load(self):
        self.todo = 'load'
        self.parent.old_scene = self

        self.sidebar.pop_buttons()
        self.parent.pop_handlers()

        self.change_scene(file_scene.FileScene(self.parent))

    def from_file_scene(self, path):
        if self.todo == 'load':
            pass
        elif self.todo == 'save':
            pass

        self.parent.push_handlers(self.sidebar)
        self.sidebar.push_buttons()

    def write(self, path):
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_collision_mode(self):
        self.collision_mode = True

        for ent, tile in self.map_tiles.values():
            if not ent in self.collision:
                ent.sprite.opacity = 100

    def remove_collision_mode(self):
        self.collision_mode = False

        for ent, tile in self.map_tiles.values():
            ent.sprite.opacity = 255

            if ent in self.collision:
                ent.sprite.color = (255, 255, 255)

    def move_scene(self, dx, dy):
        self.scene_pos[0] += dx
        self.scene_pos[1] += dy

        for entity in self.entities:
            if entity.world:
                entity.move(-dx, -dy)

        self.init()

    def move_scene_to(self, x, y):
        for entity in self.entities:
            entity.move(*self.scene_pos)
            entity.move(-x, -y)
        
        self.scene_pos = (x, y)

    def on_text(self, text):
        if text in ('d', 'D'):
            self.move_scene(SCROLL_SPEED, 0)
        elif text in ('a', 'A'):
            self.move_scene(-SCROLL_SPEED, 0)
        elif text in ('w', 'W'):
            self.move_scene(0, SCROLL_SPEED)
        elif text in ('s', 'S'):
            self.move_scene(0, -SCROLL_SPEED)
        elif text in ('c', 'C'):
            if self.collision_mode:
                self.remove_collision_mode()
            else:
                self.set_collision_mode()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.sidebar.sidebar_rect.collide_point(x, y):
            ix = (x + self.scene_pos[0]) // TILE_SIZE
            iy = (y + self.scene_pos[1]) // TILE_SIZE

            if self.sidebar.selected != None and not self.collision_mode:
                if (ix, iy) in self.map_tiles:
                    self.data["data"].remove(self.entities[(ix, iy)].data_reference)
                    self.entities.delete((ix, iy))
                    del self.map_tiles[(ix, iy)]

                if self.tiles[self.sidebar.selected][1] != 'x':
                    ent = Entity(self, self.tiles[self.sidebar.selected][0],
                        ix * TILE_SIZE - self.scene_pos[0], iy * TILE_SIZE - self.scene_pos[1],
                        batch=self.batch, group=self.groups['tiles'])

                    self.map_tiles[(ix, iy)] = (ent, self.tiles[self.sidebar.selected][1])

                    ent_entry = {"x": ix, "y": iy, "labels": [], "type": self.tiles[self.sidebar.selected][1], "offset": [0, 0]}
                    self.data["data"].append(ent_entry)

                    ent.data_reference = ent_entry

                    self.entities[(ix, iy)] = ent
            elif self.collision_mode:
                if (ix, iy) in self.map_tiles:
                    ent = self.entities[(ix, iy)]
                    if ent in self.collision:
                        self.collision.remove(ent)
                        ent.data_reference["labels"].remove("collision")
                        ent.sprite.opacity = 100
                    else:
                        self.collision.append(ent)
                        ent.data_reference["labels"].append("collision")
                        ent.sprite.opacity = 255
