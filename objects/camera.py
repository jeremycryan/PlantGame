import constants as c


class Camera:

    def __init__(self):
        self.zoom = 1.0
        self.x = 0
        self.y = 0
        self.target_x = self.x
        self.target_y = self.y

        self.pan_p = 0.05
        self.pan_i = 0.002
        self.pan_d = -0.1

        self.x_integral = 0
        self.x_derivative = 0
        self.y_integral = 0
        self.y_derivative = 0

    def set_position(self, x, y):
        self.x, self.y = x, y

    def set_zoom(self, zoom):
        self.zoom = zoom

    def set_target_position(self, x, y):
        self.target_x = x
        self.target_y = y

    def grid_to_screen(self, x, y):
        x_scale, y_scale = c.TILE_SIZE
        screen_x = (x - self.x) * x_scale * self.zoom + c.WINDOW_WIDTH//2 - c.TILE_WIDTH//2
        screen_y = (y - self.y) * y_scale * self.zoom + c.WINDOW_HEIGHT//2 - c.TILE_HEIGHT//2
        return int(screen_x), int(screen_y)

    def update(self, dt, events):
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        self.x_integral += dx * dt
        self.x_derivative = dx * self.pan_p + self.x_integral * self.pan_i + self.x_derivative * self.pan_d
        self.x += self.x_derivative

        self.y_integral += dy * dt
        self.y_derivative = dy * self.pan_p + self.y_integral * self.pan_i + self.y_derivative * self.pan_d
        self.y += self.y_derivative