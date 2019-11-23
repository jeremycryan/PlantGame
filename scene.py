# Each Frame represents a particular game screen, menu,
# level, or view. The Game object switches between them.

import random

import constants as c
from objects.camera import Camera


class Scene:

    def __init__(self, game):
        self.game = game
        self.camera = Camera()
        self.image_dict = {}
        self.age = 0

    def load_image(self, label):
        """ Returns an image if it exists in self.image_dict. Otherwise,
            loads it from the game object.
        """
        if label not in self.image_dict:
            self.image_dict[label] = self.game.load_image(label)
        return self.image_dict[label]

    def update(self, dt, events):
        """ Update the scene based on a time step, dt, and a list of PyGame events """
        self.age += dt

    def draw(self, surface):
        """ Draws the state of the scene onto a provided PyGame Surface. """
        if not hasattr(self, "color"):
            self.color = random.choice(c.COLORS)
        surface.fill(self.color)

    def get_next_scene(self):
        """ Returns the class for the next scene, only if the current scene is completed.
            Otherwise, returns None.
        """
        if self.age > 2:
            return Scene
        return None
