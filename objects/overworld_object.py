import pygame

import random

import constants as c
from sprite_tools import Sprite, SpriteSheet
from objects.plant import Jute, BostonFern, Orchid, Strawberry, Dirt


class OverWorldObject:

    def __init__(self, scene):
        self.scene = scene
        self.priority = 0
        self.blocking = False
        self.interactive = False


class StaticOverWorldObject(OverWorldObject):
    """ Subclass of OverWorldObject with no animations. """

    def __init__(self, scene, key):
        super().__init__(scene)
        self.sprite = self.scene.load_image(key)
        self.scale((64, 64), c.TILE_SIZE)
        self.width, self.height = self.sprite.get_width(), self.sprite.get_height()

    def scale(self, original_tile_size, new_tile_size):
        """ Scales the sprite based on two tuples of sizes.

            e.g. A sprite was drawn for tile size 64x64, but should be rendered as 48x48.
            Call sprite.scale((64, 64), (48, 48))
        """
        new_width = int(self.sprite.get_width() * new_tile_size[0] / original_tile_size[0])
        new_height = int(self.sprite.get_height() * new_tile_size[1] / original_tile_size[1])
        self.sprite = pygame.transform.scale(self.sprite, (new_width, new_height))

    def draw(self, surface, x, y):
        x_with_offset = x + c.TILE_WIDTH//2 - self.width//2
        y_with_offset = y + c.TILE_HEIGHT//2 - self.height//2
        surface.blit(self.sprite, (x_with_offset, y_with_offset))


class Wall(StaticOverWorldObject):

    def __init__(self, scene):
        super().__init__(scene, "wall")
        self.priority = 1
        self.blocking = True


class Floor(StaticOverWorldObject):

    def __init__(self, scene):
        super().__init__(scene, "floor")
        self.priority = 0


class AnimatedOverWorldObject(OverWorldObject):
    """ Subclass of OverWorldObject with no animations. """

    def __init__(self, scene, sprite):
        super().__init__(scene)
        self.sprite = sprite

    def draw(self, surface, x, y):
        x_offset = c.TILE_WIDTH//2 - self.sprite.get_size()[0]//2
        y_offset = c.TILE_HEIGHT//2 - self.sprite.get_size()[1]//2
        self.sprite.set_position((x + x_offset, y + y_offset))
        self.sprite.draw(surface)

    def update(self, dt, events):
        self.sprite.update(dt)


class Bed(StaticOverWorldObject):
    def __init__(self, scene):
        super().__init__(scene, "Bed")
        self.priority = 1
        self.blocking = True
        self.interactive = True

    def touch(self):
        self.scene.next_day()


class Plot(AnimatedOverWorldObject):

    def __init__(self, scene):
        self.scene = scene
        self.id = scene.get_id("plot")
        self.plant = scene.game.state.plots[self.id].plant
        self.sprite = self.get_sprite_from_plant()
        self.state = self.plant.state
        super().__init__(scene, self.sprite)

        self.blocking = True
        self.interactive = True

    def touch(self):
        """ Run this when the player tries to interact. """
        if self.scene.dialogue_box.hidden:
            self.scene.dialogue_box.load_plant_menu(self.plant.state, self.scene.game.state.plots[self.id].plant.name, self)
            self.update(0, [])

    def plant_seed(self):
        self.scene.game.state.plots[self.id].plant = random.choice([Jute(self.scene.game),
                                                                    Orchid(self.scene.game),
                                                                    Strawberry(self.scene.game),
                                                                    BostonFern(self.scene.game)])

    def remove_seed(self):
        self.scene.game.state.plots[self.id].plant = Dirt(self.scene.game)

    def update(self, dt, events):
        super().update(dt, events)
        self.update_plant_state()

    def get_sprite_from_plant(self):
        plant = self.plant
        sprite = Sprite(4)
        if plant.name == "Empty":
            key = plant.name
        elif plant.state == c.SEED:
            key = "Seed"
        else:
            key = plant.name + str(plant.state)
        sheet = SpriteSheet(self.scene.load_image(key), (1, 1), 1)
        sprite.add_animation({"idle": sheet})
        sprite.start_animation("idle")
        return sprite

    def update_plant_state(self):
        if self.plant is not self.scene.game.state.plots[self.id].plant:
            self.plant = self.scene.game.state.plots[self.id].plant
            self.sprite = self.get_sprite_from_plant()
            self.state = self.plant.state

        if self.state != self.plant.state:
            self.sprite = self.get_sprite_from_plant()
            self.state = self.plant.state

