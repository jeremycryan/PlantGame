from scene import Scene
from objects.player import Player
from objects.map import Map
from objects.camera import Camera


class OverWorld(Scene):

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.map = Map(self)
        self.player = Player(self)
        self.camera = Camera()
        self.objects = [self.player,
                        self.camera]

    def draw(self, surface):
        surface.fill((100, 150, 200))
        self.map.draw()

    def get_next_scene(self):
        return None

    def update(self, dt, events):
        super().update(dt, events)
        for item in self.objects:
            item.update(dt, events)
        self.camera.set_position(self.player.draw_x, self.player.draw_y)
