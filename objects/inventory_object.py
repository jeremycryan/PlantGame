import objects.plant as plants


class InventoryObject:
    def __init__(self, game):
        self.game = game
        self.name = "Generic Item"
        self.description = "This item exists, but has no use."
        self.givable = False
        self.plantable = False


class Seeds(InventoryObject):
    def __init__(self, game):
        super().__init__(game)
        self.plantable = True
        self.name = "Generic seeds"
        self.description = "Go feed them to a generic bird or something."

    def plant(self):
        raise NotImplementedError("Must override plant method in seed subclass.")


class StrawberrySeeds(Seeds):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Strawberry Seeds"
        self.description = "Half of them will bloom into berries. The rest will grow into straw."

    def plant(self):
        return plants.Strawberry(self.game)


class JuteSeeds(Seeds):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Jute Seeds"
        self.description = "Does jute have seeds? It's better not to ask these questions."

    def plant(self):
        return plants.Jute(self.game)


class BostonFernSeeds(Seeds):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Boston Fern Seeds"
        self.description = "These seeds look like they will produce a lot of oxygen when they're older."

    def plant(self):
        return plants.BostonFern(self.game)


class OrchidSeeds(Seeds):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Orchid Seeds"
        self.description = "One day, these will be pretty flowers. But now, they're just tiny lumps."

    def plant(self):
        return plants.Orchid(self.game)


class Strawberry(InventoryObject):
    def __init__(self, game):
        super().__init__(game)
        self.givable = True
        self.name = "Strawberry"
        self.description = "A small, sweet berry."


class Orchid(InventoryObject):
    def __init__(self, game):
        super().__init__(game)
        self.givable = True
        self.name = "Orchid"
        self.description = "Perhaps someone will want to smell this."


class Twine(InventoryObject):
    def __init__(self, game):
        super().__init__(game)
        self.givable = True
        self.name = "Twine"
        self.description = "It's long and fibrous. Looks tasty."


