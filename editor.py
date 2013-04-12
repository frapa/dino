import os
import sys
import pyglet
from lib.scenes.editor_scene import EditorScene
import lib.globe as globe

class App(pyglet.window.Window):
    def __init__(self):
        super(App, self).__init__(864, 624, caption="Editor", resizable=True)
        
        # share the window as a global variable
        globe.window = self
        
        # current scene
        self.scene = EditorScene(self)
        self.push_handlers(self.scene)
        #self.scene.start()

if __name__ == '__main__':
    globe.path = os.path.split(os.path.join(os.getcwd(), __file__))[0]

    pyglet.resource.add_font('resources/fonts/DroidSans.ttf')

    try:
        globe.map_path = sys.argv[1]
    except IndexError:
        globe.map_path = None

    window = App()
    pyglet.app.run()
