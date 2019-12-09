import pygame

import constants as c
from objects.character import Character


class Player(Character):

    def __init__(self, scene, pos=(3, 3)):
        self.name = "Player"
        super().__init__(scene, pos=pos)
        self.priority = 3

        self.press_stack = [None]  # Stack of keyboard commands, with most recent press last
        self.control_dict = {pygame.K_UP: c.UP,
                             pygame.K_DOWN: c.DOWN,
                             pygame.K_LEFT: c.LEFT,
                             pygame.K_RIGHT: c.RIGHT,
                             None: c.NO_DIRECTION}
        self.interact_key = pygame.K_SPACE

    def check_events(self, events):
        """ Checks events for control inputs. """
        for event in events:

            # Push events onto the stack for keydowns
            if event.type == pygame.KEYDOWN:
                if event.key in self.control_dict:
                    self.press_stack.append(event.key)

                if event.key == self.interact_key:
                    facing = self.x + self.face_direction[0], self.y + self.face_direction[1]
                    facing_contents = self.scene.map.get_cell(*facing)
                    for item in facing_contents:
                        if item.interactive:
                            self.interact(item)

                if event.key == pygame.K_c:
                    self.scene.next_day()

            # And remove from stack for keyups
            if event.type == pygame.KEYUP:
                if event.key in self.press_stack:
                    self.press_stack.remove(event.key)

    def interact(self, other):
        other.touch()

    def direction(self):
        if not self.scene.game.enable_player_movement:
            return c.NO_DIRECTION
        return self.control_dict[self.press_stack[-1]]
