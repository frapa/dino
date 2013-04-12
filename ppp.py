import os
import pyglet
from lib.scenes.loading_scene import LoadingScene
from lib.scenes.game_scene import GameScene
import lib.globe as globe

fps_list = []

class App(pyglet.window.Window):
    def __init__(self):
        super(App, self).__init__(1024, 600)#fullscreen=True)
        
        # share the window as a global variable
        globe.window = self
        
        # current scene
        self.scene = LoadingScene(self, 'maps/test2.json')
        self.push_handlers(self.scene)

        pyglet.clock.schedule_interval(self.show_fps, 2)

    def show_fps(self, dt):
        fps = pyglet.clock.get_fps()
        fps_list.append(fps)
        print fps

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

        if hasattr(self.scene, 'on_key_press'):
            self.scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if hasattr(self.scene, 'on_key_release'):
            self.scene.on_key_release(symbol, modifiers)

    def on_draw(self):
        self.clear()

        self.scene.batch.draw()

if __name__ == '__main__':
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    globe.path = os.path.split(os.path.join(os.getcwd(), __file__))[0]

    window = App()
    pyglet.app.run()

    if fps_list:
        print "average:", sum(fps_list) / len(fps_list)
