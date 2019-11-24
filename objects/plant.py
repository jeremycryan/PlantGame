import constants as c


class Plant:
    """ This class handles the logic and state of a single plant. Graphics are handled by the
        Plot object in overworld_object and by a to-be-implemented scene for close-ups.
    """

    def __init__(self):
        self.age = 0
        self.state = c.SEED
        self.sprout_age = 1
        self.mature_age = 3
        self.death_age = 7

    def cycle(self):
        self.age += 1

    def get_state(self):
        if self.age < self.sprout_age:
            return c.SEED
        elif self.age < self.mature_age:
            return c.SPROUT
        elif self.age < self.death_age:
            return c.MATURE
        else:
            return c.DEAD