import numpy as np
from itertools import product

FPS = 2
SITE_WIDTH_IN_CELLS = 20
SITE_HEIGHT_IN_CELLS = 20

BORDER_WIDTH = 1
WIDTH_IN_CELLS = SITE_HEIGHT_IN_CELLS + (BORDER_WIDTH * 2)
TITLE_HEIGHT = 0
HEIGHT_IN_CELLS = SITE_HEIGHT_IN_CELLS + (BORDER_WIDTH * 2) + TITLE_HEIGHT

CELLSIZE = 40
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

HEADLESS_MODE = True
NUM_DRONES = 10
NUM_SITES = 10
FEATURE_RATIO_VARIANCE = 5
NUM_TIMESTEPS = 10
TARGET_COLOR_RATIO = [80, 10, 10]

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 100,  100,  100)
LIGHTGRAY = ( 200,  200,  200)
MAGENTA   = ( 255,  0, 255)
BLUE      = (  0,   0, 255)
CYAN      = (  0, 255, 255)
YELLOW    = ( 255,  255, 0)
ORANGE    = ( 255,  127, 0)
GRAY      = (200, 200, 200)
BGCOLOR = LIGHTGRAY

#Tile coloring

LEFT = 1
DOWN = 2
RIGHT = 3
UP = 4

# define possibility candidates matrix K
possible_range = np.arange(0.1, 1.0, 0.1)
colors = []
for p in product(possible_range, repeat=3):
    if np.isclose(sum(p), 1.0):
        colors.append(p)
K = np.array(colors)        