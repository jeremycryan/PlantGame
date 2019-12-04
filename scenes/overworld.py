from scene import Scene
from objects.player import Player
from objects.character import Rando
from objects.map import Map
from objects.camera import Camera
from objects.dialogue_box import DialogueBox


class OverWorld(Scene):

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.map = Map(self)
        self.player = Player(self)
        self.characters = [Rando(self, pos=(8, 5))]
        self.camera = Camera()
        self.dialogue_box = DialogueBox(self)
        self.objects = [self.player, self.camera] + self.characters + self.map.get_plots()

    def draw(self, surface):
        surface.fill((100, 150, 200))
        self.map.draw()
        self.dialogue_box.draw()

    def get_next_scene(self):
        return None

    def update(self, dt, events):
        super().update(dt, events)
        for item in self.objects:
            item.update(dt, events)
        self.camera.set_target_position(self.player.draw_x, self.player.draw_y)
        self.dialogue_box.update(dt, events)
