FPS = 2
WINDOWWIDTH = 900
WINDOWHEIGHT = 900
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
WIDTH_IN_CELLS = int(WINDOWWIDTH / CELLSIZE)
HEIGHT_IN_CELLS = int(WINDOWHEIGHT / CELLSIZE)
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

LEFT = 1
DOWN = 2
RIGHT = 3
UP = 4
