import constants as c


class Camera:

    def __init__(self):
        self.zoom = 1.0
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x, self.y = x, y

    def set_zoom(self, zoom):
        self.zoom = zoom

    def grid_to_screen(self, x, y):
        x_scale, y_scale = c.TILE_SIZE
        screen_x = (x - self.x) * x_scale * self.zoom + c.WINDOW_WIDTH//2 - c.TILE_WIDTH//2
        screen_y = (y - self.y) * y_scale * self.zoom + c.WINDOW_HEIGHT//2 - c.TILE_HEIGHT//2
        return int(screen_x), int(screen_y)

    def update(self, dt, events):
        pass