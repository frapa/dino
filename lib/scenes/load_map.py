import json
import pyglet

from ..entity.rect import Rect
from ..entity.entity import Entity
from ..entity.char import Char
from ..entity.enemy import BaseEnemy
from .. import globe

# loads map it supposes it is called by a standard game scene class
def load_map(scene, map_file, load_chars=True):
    with pyglet.resource.file(map_file) as f:
        data = json.load(f)
        block_group = scene.groups['environment']

        # load map features
        for e in data['static_entities']:
            ent = None

            # image objects 
            if e['class'] == 'sprite':
                if e.has_key('rect'):
                    ent = Entity(scene, 'tiles/' + e['type'] + '.png', x=e['x'], y=e['y'],
                        batch=scene.batch, group=scene.groups['tiles'],
                        rect=Rect(*e['rect']))
                else:
                    ent = Entity(scene, 'tiles/' + e['type'] + '.png', x=e['x'], y=e['y'],
                        batch=scene.batch, group=scene.groups['tiles'])

                #ent.move(*e['offset'])
            # GL_QUADS used to fill some places
            elif e["class"] == 'block':
                if e.has_key('rect'):
                    ent = Entity(scene, e, batch=scene.batch, group=block_group,
                        rect=Rect(*e['rect']))
                else:
                    ent = Entity(scene, e, batch=scene.batch, group=block_group)

                # lower group so that drawing do not get confudes
                block_group = pyglet.graphics.OrderedGroup(order=block_group.order - 1)
            # COLLISION RECTS
            elif e["class"] == 'collision':
                ent = Entity(scene, rect=Rect(*e['rect']))
                ent.friction = e['friction']

                scene.collision.append(ent)

            if e.has_key("labels"):
                if 'collision' in e['labels'] and e["class"] != 'collision':
                    scene.collision.append(ent)
                
                if 'dangerous' in e['labels']:
                    scene.dangerous.append(ent)

        # load sky
        if data.has_key('sky_color'):
            w = globe.window.width
            h = globe.window.height

            if len(data["sky_color"]) == 3:
                color = data["sky_color"] * 4
            elif len(data["sky_color"]) == 6:
                color = data['sky_color'][:3] * 2 + data['sky_color'][3:] * 2
            elif len(data["sky_color"]) == 12:
                color = data['sky_color']

            scene.sky = scene.batch.add(4, pyglet.gl.GL_QUADS, scene.groups['sky'],
                ('v2f', (0, 0, w, 0, w, h, 0, h)),
                ('c3B', color)
            )

        if load_chars:
            # create charater
            name = 'ciccia'
            # +1 e -2 sono per far passare il dino in buchi di una tile
            char_rect = Rect(data['player_pos']['x'] + 1, data['player_pos']['y'], 48 - 2, 48 - 2)
            scene.char = Char(scene, name, rect=char_rect, group=scene.groups['chars'], add=False)

            scene.char.set_offset(-1, -1)
            scene.char.enable_gravity()

            scene.char.sprite.image = scene.char.images[name + '_jump_right']
            
            # enemy
            #name = 'chicken'
            #char_rect = Rect(500, 100, 48, 48)
            #enemy = BaseEnemy(scene, name, rect=char_rect, batch=scene.batch, group=scene.groups['chars'])

            #enemy.set_offset(0, -1)
            #enemy.enable_gravity()
