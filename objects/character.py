import random

import helpers as h
import constants as c
from objects.overworld_object import OverWorldObject


class Character(OverWorldObject):
    def __init__(self, scene, pos=(3, 3)):
        super().__init__(scene)
        self.priority = 3
        self.blocking = True

        self.sprite = self.scene.load_image("player_temp")

        self.x = pos[0]
        self.y = pos[1]
        self.scene.map.add_to_cell(self, self.x, self.y)
        self.draw_x = self.x
        self.draw_y = self.y
        self.prev_x = self.x
        self.prev_y = self.y
        self.shadow = CharacterShadow(scene, self)
        self.scene.map.add_to_cell(self.shadow, self.x, self.y)

        self.since_move = 0
        self.move_speed = 5

        self.in_motion = False
        self.next_direction = c.NO_DIRECTION

    def draw(self, surface):
        draw_x, draw_y = self.scene.camera.grid_to_screen(self.draw_x, self.draw_y)
        surface.blit(self.sprite, (draw_x, draw_y))

    def update(self, dt, events):
        self.check_events(events)
        self.since_move += dt
        self.draw_x = h.approach(self.draw_x, self.x, self.move_speed*dt)
        self.draw_y = h.approach(self.draw_y, self.y, self.move_speed*dt)
        if (self.draw_x, self.draw_y) == (self.x, self.y) and (self.x, self.y) != (self.prev_x, self.prev_y):
            self.arrive()

        self.update_move(self.direction())

    def check_events(self, events):
        pass

    def direction(self):
        new_direction = self.next_direction
        self.next_direction = c.NO_DIRECTION
        return new_direction

    def arrive(self):
        """ Called when the player arrives at the target location each step. """
        self.in_motion = False
        self.scene.map.remove_from_cell(self.shadow, self.prev_x, self.prev_y)
        self.scene.map.add_to_cell(self.shadow, self.x, self.y)
        self.prev_x, self.prev_y = self.x, self.y

    def move(self, direction):
        """ Queues a movement in the direction for the character."""
        self.next_direction = direction

    def update_move(self, direction):
        """ Move the character one square in a direction. """
        self.scene.map.remove_from_cell(self, self.x, self.y)
        if not self.in_motion and direction is not c.NO_DIRECTION:
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]

            if not self.scene.map.cell_is_blocking(new_x, new_y):
                self.prev_x = self.x
                self.prev_y = self.y
                self.x += direction[0]
                self.y += direction[1]
                self.since_move = 0
                self.in_motion = True

        self.scene.map.add_to_cell(self, self.x, self.y)


class Rando(Character):
    def update(self, dt, events):
        if self.since_move > 2:
            self.move(random.choice(c.DIRECTIONS))
        super().update(dt, events)


class CharacterShadow(OverWorldObject):

    def __init__(self, scene, character):
        super().__init__(scene)
        self.character = character
        self.priority = 3
        self.blocking = True

    def draw(self, surf, x, y):
        self.character.draw(surf)