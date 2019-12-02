from objects.plant import Dirt


class Plot:
    """ No, not the story kind. We don't have one of those.

        This object serves as a container for Plant objects.
    """

    def __init__(self, game):
        self.game = game
        self.plant = Dirt(game)

    def cycle(self):
        self.plant.cycle()