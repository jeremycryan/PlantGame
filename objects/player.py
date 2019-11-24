import pygame

import time

import constants as c
import helpers as h
from objects.overworld_object import OverWorldObject
from objects.character import Character


class Player(Character):

    def __init__(self, scene):
        super().__init__(scene)
        self.priority = 3

        self.sprite = self.scene.load_image("player_temp")

        self.press_stack = [None]  # Stack of keyboard commands, with most recent press last
        self.control_dict = {pygame.K_UP: c.UP,
                             pygame.K_DOWN: c.DOWN,
                             pygame.K_LEFT: c.LEFT,
                             pygame.K_RIGHT: c.RIGHT,
                             None: c.NO_DIRECTION}

    def check_events(self, events):
        """ Checks events for control inputs. """
        for event in events:

            # Push events onto the stack for keydowns
            if event.type == pygame.KEYDOWN:
                if event.key in self.control_dict:
                    self.press_stack.append(event.key)

            # And remove from stack for keyups
            if event.type == pygame.KEYUP:
                if event.key in self.press_stack:
                    self.press_stack.remove(event.key)

    def direction(self):
        return self.control_dict[self.press_stack[-1]]