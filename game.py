# The main Game object that runs the game and manages Frames.

import sys
import time
import random

import pygame

import constants as c
from scenes.overworld import OverWorld
from objects.plot import Plot
from objects.plant import Dirt
import objects.inventory_object as inv


class Game:

    screen = None
    shade_alpha = None
    shade_target = None
    enable_player_movement = True

    def __init__(self):
        pygame.init()
        self.state = GameState(self)
        self.shade = self.initialize_shade()
        self.image_dict = {}
        self.initialize_screen()
        self.active_scene = OverWorld(self)
        self.run()

    def initialize_screen(self):
        """ Creates a PyGame window and sets the caption """
        self.screen = pygame.display.set_mode(c.WINDOW_SIZE, pygame.FULLSCREEN)
        pygame.display.set_caption(c.WINDOW_CAPTION)

    def initialize_shade(self):
        shade = pygame.Surface(c.WINDOW_SIZE)
        shade.fill(c.BLACK)
        self.shade_alpha = c.SHADE_ON
        self.shade_target = c.SHADE_OFF
        return shade

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
            dt = min(now - then, c.MIN_TIME_STEP)  # If too much time has passed, lag the game
            then = now
            events = pygame.event.get()

            # Switch to next scene, if ready
            next_scene = self.active_scene.get_next_scene()
            if next_scene is not None:
                self.shade_target = c.SHADE_ON
                self.enable_player_movement = False
                if self.shade_alpha == c.SHADE_ON:
                    self.active_scene = next_scene(self)

            # Run updates and draw to screen
            self.check_global_events(events)
            self.active_scene.update(dt, events)
            self.active_scene.draw(self.screen)
            self.update_and_draw_shade(dt)

            pygame.display.flip()

    def update_and_draw_shade(self, dt):
        if self.shade_target < self.shade_alpha:
            self.shade_alpha = max(c.SHADE_OFF, self.shade_alpha - dt*c.SHADE_SPEED)
        elif self.shade_target > self.shade_alpha:
            self.shade_alpha = min(c.SHADE_ON, self.shade_alpha + dt*c.SHADE_SPEED)
        self.shade.set_alpha(self.shade_alpha)
        self.screen.blit(self.shade, (0, 0))

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
        self.player_inventory = [inv.StrawberrySeeds(self.game),
                                 inv.BostonFernSeeds(self.game),
                                 inv.OrchidSeeds(self.game),
                                 inv.JuteSeeds(self.game)]
        self.last_player_position = (3, 3)

    def add_to_inventory(self, item):
        self.player_inventory.append(item)

    def cycle(self):
        """ Updates all game state objects one cycle. """
        for plot in self.plots:
            plot.cycle()
        self.oxygen -= 5
        self.game.shade_target = c.SHADE_OFF
        self.game.enable_player_movement = True
        print("A day passes. Oxygen at %s" % self.oxygen)

    def add_oxygen(self, amt):
        self.oxygen += amt

    def remove_plant(self, plant):
        """ Removes a plant from any plots it exists in. """
        for plot in self.plots:
            if plot.plant == plant:
                plot.plant = Dirt(self.game)


if __name__ == "__main__":
    Game()