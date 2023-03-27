FPS = 2
SITE_WIDTH_IN_CELLS = 20
SITE_HEIGHT_IN_CELLS = 20

BORDER_WIDTH = 1
WIDTH_IN_CELLS = SITE_HEIGHT_IN_CELLS + (BORDER_WIDTH * 2)
TITLE_HEIGHT = 0
HEIGHT_IN_CELLS = SITE_HEIGHT_IN_CELLS + (BORDER_WIDTH * 2) + TITLE_HEIGHT

CELLSIZE = 40
WINDOWWIDTH = 800 + (BORDER_WIDTH * 2 * CELLSIZE)
WINDOWHEIGHT = 800 + (BORDER_WIDTH * 2 * CELLSIZE) + (TITLE_HEIGHT * CELLSIZE)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

NUM_ROOMBAS = 10

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 100,  100,  100)
LIGHTGRAY  = ( 200,  200,  200)
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

