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
        self.game.state.cycle()
        self.map = Map(self)
        self.player = Player(self, pos=self.game.state.last_player_position)
        self.characters = [Rando(self, pos=(8, 5))]
        self.camera = Camera(pos=self.game.state.last_player_position)
        self.dialogue_box = DialogueBox(self)
        self.dialogue_box.hide()
        self.objects = [self.player, self.camera] + self.characters + self.map.get_plots()
        self.next_scene = None

    def draw(self, surface):
        surface.fill((20, 20, 60))
        self.map.draw()
        self.dialogue_box.draw()

    def next_day(self):
        self.next_scene = OverWorld
        self.game.state.last_player_position = self.player.x, self.player.y

    def get_next_scene(self):
        return self.next_scene

    def update(self, dt, events):
        super().update(dt, events)
        for item in self.objects:
            item.update(dt, events)
        self.camera.set_target_position(self.player.draw_x, self.player.draw_y)
        self.dialogue_box.update(dt, events)
