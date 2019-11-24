import constants as c
import helpers as h
from objects.overworld_object import Wall, Floor, Plot


class Map:

    def __init__(self, scene):
        self.scene = scene
        self.mapping = {c.WALL_CHAR: Wall,
                        c.FLOOR_CHAR: Floor,
                        c.PLOT_CHAR: Plot}
        self.container = self.generate_layout()

    def generate_layout(self):
        """ Returns a y by x array of empty lists. """
        path = c.TEXT_PATH_DICT["ship_map"]
        with open(path) as f:
            lines = [line.strip() for line in f.readlines()]

        # Generate grid of same size as text file
        width = len(lines[0])
        height = len(lines)
        empty = [[[] for _ in line] for line in lines]

        # Populate with objects from self.mapping
        for x in range(width):
            for y in range(height):
                map_char = lines[y][x]
                new_item = self.mapping[map_char](self.scene)
                empty[y][x].append(new_item)

        return empty

    def draw(self):
        for y, row in enumerate(self.container):
            for x, cell in enumerate(row):
                cell = sorted(cell, key=h.priority)
                for item in cell:
                    if hasattr(item, "x") and hasattr(item, "y"):
                        item.draw(self.scene.game.screen)
                    else:
                        item.draw(self.scene.game.screen,
                                  *self.scene.camera.grid_to_screen(x, y))

    def get_cell(self, x, y):
        """ Gets the contents of the cell located at x, y. """
        return self.container[y][x]

    def add_to_cell(self, item, x, y):
        self.get_cell(x, y).append(item)
        self.container[y][x] = sorted(self.container[y][x], key=h.priority)

    def remove_from_cell(self, item, x, y):
        """ Removes the specified item from cell x, y if it exists.
            Returns True if the object was removed successfully.
        """
        if item in self.get_cell(x, y):
            self.get_cell(x, y).remove(item)
            return True
        return False

    def cell_is_blocking(self, x, y):
        """ Returns True if any item in the cell x, y is blocking. """
        return any([item.blocking for item in self.container[y][x]])
