import os

#  Screen settings
WINDOW_CAPTION = "Plant Simulator 2000"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

# Asset loading
ASSETS_PATH = "assets"
IMAGE_PATH_DICT = {"player_temp": os.path.join(ASSETS_PATH, "player_temp.png"),
                   "wall": os.path.join(ASSETS_PATH, "wall_placeholder.png"),
                   "floor": os.path.join(ASSETS_PATH, "floor_placeholder.png")}
MAP_PATH_DICT = {"ship_map": os.path.join(ASSETS_PATH, "ship.txt")}

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = (RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, GRAY, WHITE, BLACK)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
NO_DIRECTION = (0, 0)

# Text mapping
WALL_CHAR = "W"
FLOOR_CHAR = "."
TILE_WIDTH = 64
TILE_HEIGHT = 64
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT)