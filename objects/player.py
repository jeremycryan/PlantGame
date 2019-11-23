import pygame

import time

import constants as c
import helpers as h
from objects.overworld_object import OverWorldObject


class Player(OverWorldObject):

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

        self.x = 3
        self.y = 3
        self.scene.map.add_to_cell(self, self.x, self.y)
        self.draw_x = self.x
        self.draw_y = self.y

        self.move_latency = 0.2
        self.since_move = self.move_latency
        self.move_speed = 1/self.move_latency

    def draw(self, surface):
        draw_x, draw_y = self.scene.camera.grid_to_screen(self.draw_x, self.draw_y)
        surface.blit(self.sprite, (draw_x, draw_y))

    def update(self, dt, events):
        self.check_events(events)
        self.since_move += dt
        self.draw_x = h.approach(self.draw_x, self.x, self.move_speed*dt)
        self.draw_y = h.approach(self.draw_y, self.y, self.move_speed*dt)
        self.move(dt)

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

    def move(self, dt):
        """ Move the player in a direction. """
        direction = self.control_dict[self.press_stack[-1]]
        self.scene.map.remove_from_cell(self, self.x, self.y)
        if self.since_move >= self.move_latency and direction is not c.NO_DIRECTION:
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]

            if not self.scene.map.cell_is_blocking(new_x, new_y):
                self.x += direction[0]
                self.y += direction[1]
                self.since_move = 0

        self.scene.map.add_to_cell(self, self.x, self.y)