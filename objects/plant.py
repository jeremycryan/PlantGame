import constants as c

import objects.inventory_object as inv
from sprite_tools import SpriteSheet


class Plant:
    """ This class handles the logic and state of a single plant. Graphics are handled by the
        Plot object in overworld_object and by a to-be-implemented scene for close-ups.
    """

    def __init__(self, game):
        self.game = game
        self.age = 0
        self.state = c.SEED
        self.sprout_age = 1
        self.mature_age = 3
        self.death_age = 7
        self.oxygen_production = 2
        self.fruit_period = None

        self.name = "Plant"

    def cycle(self):
        self.age += 1
        if self.state == c.MATURE:
            self.game.state.add_oxygen(self.oxygen_production)
        self.state = self.get_state()

    def set_life_attributes(self, **kwargs):
        if "sprout_age" in kwargs:
            self.sprout_age = kwargs["sprout_age"]
        if "mature_age" in kwargs:
            self.mature_age = kwargs["mature_age"]
        if "death_age" in kwargs:
            self.death_age = kwargs["death_age"]

    def prune(self):
        print("pruned")
        self.death_age += 0.5
        if self.fruit_period is not None:
            self.fruit_period -= 1

    def get_state(self):
        if self.age < self.sprout_age:
            return c.SEED
        elif self.age < self.mature_age:
            return c.SPROUT
        elif self.age < self.death_age:
            if self.fruit_period:
                if (self.age - self.mature_age) % self.fruit_period == 0:
                    return c.FRUIT
            return c.MATURE
        else:
            return c.DEAD

    def get_description(self):
        return "It's green and photosynthesizes. Whoop-de-doo."


class Jute(Plant):
    def __init__(self, game):
        super().__init__(game)
        self.set_life_attributes(sprout_age=1,
                                 mature_age=3,
                                 death_age=6)
        self.oxygen_production = 2

        self.name = "Jute"

    def get_description(self):
        return "It's tall and fibrous. Looks tasty."

    def harvest(self):
        self.game.state.remove_plant(self)
        return inv.Twine(self.game)



class BostonFern(Plant):
    def __init__(self, game):
        super().__init__(game)
        self.set_life_attributes(sprout_age=1,
                                 mature_age=5,
                                 death_age=11)
        self.oxygen_production = 12

        self.name = "Boston Fern"

    def get_description(self):
        return "It might produce a lot of oxygen, but it looks like the Green Giant vomited on your lawn."


class Orchid(Plant):
    def __init__(self, game):
        super().__init__(game)
        self.set_life_attributes(sprout_age=1,
                                 mature_age=7,
                                 death_age=9)
        self.oxygen_production = 2

        self.name = "Moth Orchid"

    def get_description(self):
        return "It definitely looks like an orchid, but it looks nothing like a moth."

    def harvest(self):
        self.game.state.remove_plant(self)
        return inv.Orchid(self.game)


class Strawberry(Plant):
    def __init__(self, game):
        super().__init__(game)
        self.set_life_attributes(sprout_age=1,
                                 mature_age=3,
                                 death_age=9)
        self.oxygen_production = 1
        self.fruit_period = 4

        self.name = "Strawberry"

    def get_description(self):
        return "One day, it's fruits might be used to sweeten the kale smoothies of suburban hipsters."

    def harvest(self):
        self.fruit_period = 4
        self.state = c.MATURE
        return inv.Strawberry(self.game)


class Dirt(Plant):
    def __init__(self, game):
        super().__init__(game)
        self.oxygen_production = 0
        self.state = c.DIRT

        self.name = "Empty"

    def get_description(self):
        return "The bare plot of soil looks up at you as if to say 'give me your seed.'"

    def get_state(self):
        return c.DIRT
