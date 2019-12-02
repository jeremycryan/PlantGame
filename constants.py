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
                   "floor": os.path.join(ASSETS_PATH, "floor_placeholder.png"),
                   "dirt_tile": os.path.join(ASSETS_PATH, "dirt_placeholder.png"),
                   "sprout_tile": os.path.join(ASSETS_PATH, "sprouts_placeholder.png"),
                   "grass_tile": os.path.join(ASSETS_PATH, "grass_placeholder.png"),
                   "player_walk_down": os.path.join(ASSETS_PATH, "captain_walk.png"),
                   "player_walk_up": os.path.join(ASSETS_PATH, "captain_walk_up.png"),
                   "player_idle_down": os.path.join(ASSETS_PATH, "captain_idle_down.png"),
                   "player_idle_up": os.path.join(ASSETS_PATH, "captain_idle_up.png"),
                   "player_walk_right": os.path.join(ASSETS_PATH, "captain_walk_right.png"),
                   "player_idle_right": os.path.join(ASSETS_PATH, "captain_idle_right.png")}
TEXT_PATH_DICT = {"ship_map": os.path.join(ASSETS_PATH, "ship.txt")}

# Dialogue loading
DIALOGUE_PATH = "dialogue/Emilia"
DIALOGUE_PATH_DICT = {"emilia_example": os.path.join(DIALOGUE_PATH, "emilia_example.txt")}

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
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# Text mapping
WALL_CHAR = "W"
FLOOR_CHAR = "."
PLOT_CHAR = "P"
TILE_WIDTH = 64
TILE_HEIGHT = 64
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT)

# Plant states
SEED = 0
SPROUT = 1
MATURE = 2
DEAD = 3
