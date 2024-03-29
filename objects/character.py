import random

import pygame
import helpers as h
import constants as c
from objects.overworld_object import OverWorldObject
from sprite_tools import Sprite, SpriteSheet
from objects.dialogue import Dialogue


class Character(OverWorldObject):
    name = None

    def __init__(self, scene, pos=(3, 3)):
        super().__init__(scene)
        self.priority = 3
        self.blocking = True
        self.interactive = True
        self.dialogue = None

        tag_dict = {"Player": "player",
                    "Emilia": "captain",
                    None: "player"}
        tag = tag_dict[self.name]

        down = SpriteSheet(scene.load_image(f"{tag}_walk_down"), (6, 1), 6)
        up = SpriteSheet(scene.load_image(f"{tag}_walk_up"), (6, 1), 6)
        down_idle = SpriteSheet(scene.load_image(f"{tag}_idle_down"), (4, 1), 4)
        up_idle = SpriteSheet(scene.load_image(f"{tag}_idle_up"), (4, 1), 4)
        right = SpriteSheet(scene.load_image(f"{tag}_walk_right"), (6, 1), 6)
        left = SpriteSheet(scene.load_image(f"{tag}_walk_right"), (6, 1), 6)
        left.reverse(1, 0)
        right_idle = SpriteSheet(scene.load_image(f"{tag}_idle_right"), (4, 1), 4)
        left_idle = SpriteSheet(scene.load_image(f"{tag}_idle_right"), (4, 1), 4)
        left_idle.reverse(1, 0)
        self.sprite = Sprite(8)
        self.sprite.add_animation({"down": down,
                                   "up": up,
                                   "down_idle": down_idle,
                                   "up_idle": up_idle,
                                   "right": right,
                                   "left": left,
                                   "right_idle": right_idle,
                                   "left_idle": left_idle})
        self.sprite.start_animation("down_idle")
        self.idles = {c.DOWN: "down_idle", c.UP: "up_idle", c.RIGHT: "right_idle", c.LEFT: "left_idle"}
        self.idle_playing = True

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
        self.move_speed = 3

        self.in_motion = False
        self.next_direction = c.NO_DIRECTION
        self.face_direction = c.DOWN
        self.last_face_direction = c.DOWN
        self.since_arrive = 999

        self.shadow_surf = pygame.Surface(c.TILE_SIZE)
        self.shadow_surf.fill(c.WHITE)
        width = int(c.TILE_WIDTH * 0.7)
        height = int(c.TILE_HEIGHT * 0.5)
        pygame.draw.ellipse(self.shadow_surf,
                            c.BLACK,
                            (c.TILE_WIDTH//2 - width//2,
                             3.2*c.TILE_HEIGHT//5 - height//2,
                             width,
                             height))
        self.shadow_surf.set_alpha(30)
        self.shadow_surf.set_colorkey(c.WHITE)

    def draw(self, surface):
        draw_x, draw_y = self.scene.camera.grid_to_screen(self.draw_x, self.draw_y)
        yoff = c.TILE_HEIGHT//1.5
        self.sprite.set_position((draw_x, draw_y - yoff))
        surface.blit(self.shadow_surf, (draw_x, draw_y))
        self.sprite.draw(surface)

    def touch(self):
        pass

    def setDialogue(self, dialogueTag):
        self.dialogue = Dialogue(dialogueTag, self.name)

    def update(self, dt, events):
        self.check_events(events)
        self.since_move += dt
        self.since_arrive += dt
        self.draw_x = h.approach(self.draw_x, self.x, self.move_speed*dt)
        self.draw_y = h.approach(self.draw_y, self.y, self.move_speed*dt)
        if (self.draw_x, self.draw_y) == (self.x, self.y) and (self.x, self.y) != (self.prev_x, self.prev_y) and self.in_motion:
            self.arrive()

        self.update_move(self.direction())

        self.sprite.update(dt)
        if self.since_arrive > 0.1 and not self.idle_playing and not self.in_motion:
            self.idle_playing = True
            if self.face_direction in self.idles:
                self.sprite.start_animation(self.idles[self.face_direction])

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
        self.since_arrive = 0

    def move(self, direction):
        """ Queues a movement in the direction for the character."""
        self.next_direction = direction

    def update_move(self, direction):
        """ Move the character one square in a direction. """
        self.scene.map.remove_from_cell(self, self.x, self.y)
        if not self.in_motion and direction is not c.NO_DIRECTION:
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]
            self.face_direction = direction

            if not self.scene.map.cell_is_blocking(new_x, new_y):
                self.prev_x = self.x
                self.prev_y = self.y
                self.x += direction[0]
                self.y += direction[1]
                self.since_move = 0
                self.in_motion = True

            self.turn(direction)

        self.scene.map.add_to_cell(self, self.x, self.y)

    def turn(self, direction):
        if direction != self.last_face_direction or self.idle_playing:
            self.idle_playing = False
            if direction == c.UP:
                self.sprite.start_animation("up")
            elif direction == c.DOWN:
                self.sprite.start_animation("down")
            elif direction == c.LEFT:
                self.sprite.start_animation("left")
            elif direction == c.RIGHT:
                self.sprite.start_animation("right")
        self.last_face_direction = direction


class Rando(Character):

    def __init__(self, scene, pos=(3, 3)):
        self.name = "Emilia"
        super().__init__(scene, pos=pos)

    def update(self, dt, events):
        if not self.in_motion and self.since_move > 3 and self.scene.dialogue_box.hidden:
            self.move(random.choice(c.DIRECTIONS))
        super().update(dt, events)

    def touch(self):
        self.scene.dialogue_box.load_character_menu("emilia_example", self.name)

        if self.scene.player.x < self.x:
            self.face_direction = c.LEFT
            self.sprite.start_animation("left_idle")
        elif self.scene.player.x > self.x:
            self.face_direction = c.RIGHT
            self.sprite.start_animation("right_idle")
        elif self.scene.player.y < self.y:
            self.face_direction = c.UP
            self.sprite.start_animation("up_idle")
        elif self.scene.player.y > self.y:
            self.face_direction = c.DOWN
            self.sprite.start_animation("down_idle")
        self.last_face_direction = self.face_direction


class CharacterShadow(OverWorldObject):

    def __init__(self, scene, character):
        super().__init__(scene)
        self.character = character
        self.priority = 3
        self.blocking = True

    def draw(self, surf, x, y):
        self.character.draw(surf)
