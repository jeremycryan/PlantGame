class InventoryObject:
    def __init__(self, scene):
        self.scene = scene
        self.name = "Generic Item"
        self.description = "This item exists, but has no use."
        self.givable = False
        self.plantable = False


class Strawberry(InventoryObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.givable = True
        self.name = "Strawberry"
        self.description = "A small, sweet berry."


class Orchid(InventoryObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.givable = True
        self.name = "Orchid"
        self.description = "Perhaps someone will want to smell this."


class Twine(InventoryObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.givable = True
        self.name = "Twine"
        self.description = "It's long and fibrous. Looks tasty."


