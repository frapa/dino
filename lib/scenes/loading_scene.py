import pyglet
import scene
import game_scene
from .. import globe as globe

class LoadingScene(scene.Scene):
    def __init__(self, parent, map_file):
        super(LoadingScene, self).__init__(parent)

        pyglet.text.Label('Loading', font_size=32,
            x=globe.window.width/2, y=globe.window.height/2,
            anchor_x='center', anchor_y='center',
            batch=self.batch)

        self.map_file = map_file

        pyglet.clock.schedule_once(self.load, 0.02)

    def load(self, interval):
        # load stuff
        self.game_scene = game_scene.GameScene(self.parent)
        
        # load map
        self.game_scene.load_map(self.map_file)

        # enter game
        self.change_scene(self.game_scene)
