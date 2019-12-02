# The main Game object that runs the game and manages Frames.

import sys
import time
import random

import pygame

import constants as c
from scenes.overworld import OverWorld
from objects.plot import Plot


class Game:

    screen = None

    def __init__(self):
        pygame.init()
        self.state = GameState(self)
        self.image_dict = {}
        self.initialize_screen()
        self.active_scene = OverWorld(self)
        self.run()

    def initialize_screen(self):
        """ Creates a PyGame window and sets the caption """
        self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        pygame.display.set_caption(c.WINDOW_CAPTION)

    def load_image(self, label):
        """ Returns an image if it exists in self.image_dict. Otherwise,
            loads it from source based on the path dictionary defined in constants.
        """
        if label not in self.image_dict:
            if label in c.IMAGE_PATH_DICT:
                self.image_dict[label] = pygame.image.load(c.IMAGE_PATH_DICT[label])
            else:
                new_surf = pygame.Surface(c.TILE_SIZE)
                new_surf.fill(random.choice(c.COLORS))
                self.image_dict[label] = new_surf
        return self.image_dict[label]

    def run(self):
        """ Runs the game's main loop. """

        then = time.time()
        time.sleep(0.001)

        while True:

            # Calculate time step and get events
            now = time.time()
            dt = now - then
            then = now
            events = pygame.event.get()

            # Switch to next scene, if ready
            next_scene = self.active_scene.get_next_scene()
            if next_scene is not None:
                print(next_scene)
                self.active_scene = next_scene(self)

            # Run updates and draw to screen
            self.check_global_events(events)
            self.active_scene.update(dt, events)
            self.active_scene.draw(self.screen)
            pygame.display.flip()

    def check_global_events(self, events):
        """ Checks game-level events. """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class GameState:

    def __init__(self, game):
        self.game = game
        self.oxygen = 100
        self.plots = [Plot(game) for _ in range(10)]

    def cycle(self):
        """ Updates all game state objects one cycle. """
        for plot in self.plots:
            plot.cycle()
        self.oxygen -= 5
        print("A day passes. Oxygen at %s" % self.oxygen)

    def add_oxygen(self, amt):
        self.oxygen += amt


if __name__ == "__main__":
    Game()