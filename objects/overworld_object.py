import constants as c


class OverWorldObject:

    def __init__(self, scene):
        self.scene = scene
        self.priority = 0
        self.blocking = False


class StaticOverWorldObject(OverWorldObject):
    """ Subclass of OverWorldObject with no animations. """

    def __init__(self, scene, key):
        super().__init__(scene)
        self.sprite = self.scene.load_image(key)
        self.width, self.height = self.sprite.get_width(), self.sprite.get_height()

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
