# Robot swarm site selection project

from vacuum import vacuum as vacuumObj
from Site import *
import enums.constants as con
import enums.walls as walls
import random, pygame, sys
from pygame.locals import *

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Swarm Site Select Simulation')


    while True:
        runGame()

def runGame():
    color_iteration_size = 0 if con.NUM_ROOMBAS < 2 else int(1530 / (con.NUM_ROOMBAS))
    all_coords     = [[x, y] for x in range(0, con.WIDTH_IN_CELLS) for y in range(0, con.HEIGHT_IN_CELLS)]
    free_locations = [x for x in all_coords if x not in walls.values]

    #init environment
    site1 = Site(0, (0,100,0))
    # print(site1)

    # initialize roombas
    curr_color = 0
    vacuums = []
    for i in range(con.NUM_ROOMBAS):
        coords = random.choice(free_locations)
        free_locations.remove(coords)
        color = ()
        if curr_color < 256:
           color = (255, curr_color, 0) 
        elif curr_color < 511:
            color = (255 - (curr_color - 255), 255, 0)
        elif curr_color < 766:
            color = (0, 255, curr_color - 510)
        elif curr_color < 1021:
            color = (0, 255 - (curr_color - 765), 255)
        elif curr_color < 1276:
            color = (curr_color - 1020, 0, 255)
        elif curr_color < 1531:
            color = (255, 0, 255 - (curr_color - 1275))
        newVacuum = vacuumObj(coords, color)
        vacuums.append(newVacuum)
        curr_color += color_iteration_size

    # generate heavy dirt
    heavy_dirt = {'values': [], 'color': (58, 31, 4)}
    for i in range(150):
        coord = random.choice(free_locations)
        heavy_dirt['values'].append(coord)
        free_locations.remove(coord)
    
    # generate normal dirt in all available spaces
    dirt = {'values': [], 'color': (75, 56, 42)}
    dirt['values'] = free_locations.copy()

    while True: 
        DISPLAYSURF.fill(con.WHITE)
        drawTiles(site1.board)
        drawGrid()
        drawStuff(walls)
        # drawDirt(heavy_dirt)
        # drawDirt(dirt)
        drawVacuums(vacuums)

        for vacuum in vacuums:
            if vacuum.current_coordinates in heavy_dirt['values']:
                dirt['values'].append(heavy_dirt['values'].pop(heavy_dirt['values'].index(vacuum.current_coordinates)))
                if vacuum.row_turn_direction == 0:
                    vacuum.row_turn_direction = random.choice([vacuum.direction - 1 if vacuum.direction > 1 else 4, vacuum.direction + 1 if vacuum.direction < 4 else 1])
            elif vacuum.current_coordinates in dirt['values']:
                dirt['values'].pop(dirt['values'].index(vacuum.current_coordinates))
                if vacuum.row_turn_direction == 0:
                    vacuum.row_turn_direction = random.choice([vacuum.direction - 1 if vacuum.direction > 1 else 4, vacuum.direction + 1 if vacuum.direction < 4 else 1])
                vacuum.move()
            else:
                vacuum.row_turn_direction = 0
                vacuum.move()
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(con.FPS)

def drawVacuums(vacuums):
    for vacuum in vacuums:
        x = vacuum.current_coordinates[0] * con.CELLSIZE
        y = vacuum.current_coordinates[1] * con.CELLSIZE
        
        pygame.draw.circle(DISPLAYSURF, (0, 0, 0), (x + (con.CELLSIZE / 2), y + (con.CELLSIZE / 2)), (con.CELLSIZE / 2))
        pygame.draw.circle(DISPLAYSURF, vacuum.color, (x + (con.CELLSIZE / 2), y + (con.CELLSIZE / 2)), (con.CELLSIZE / 2) - 2)

def drawGrid():
    for x in range(0, con.WINDOWWIDTH, con.CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, con.BLACK, (x, 0), (x, con.WINDOWHEIGHT))
    for y in range(0, con.WINDOWHEIGHT, con.CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, con.BLACK, (0, y), (con.WINDOWWIDTH, y))

def drawStuff(stuffs):
    for stuff in stuffs.values:
        stuffRect = pygame.Rect(stuff[0] * con.CELLSIZE, stuff[1] * con.CELLSIZE, con.CELLSIZE, con.CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, stuffs.color, stuffRect)

def drawDirt(dirts):
    for dirt in dirts['values']:
        dirtRect = pygame.Rect(dirt[0] * con.CELLSIZE, dirt[1] * con.CELLSIZE, con.CELLSIZE, con.CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, dirts['color'], dirtRect)

def drawTiles(board):
    color_map = {0: con.BLUE, 1: con.GREEN, 2: con.ORANGE}
    for row_index in range(len(board)):
        for col_index in range(len(board[row_index])):
            tileRect = pygame.Rect((1 + row_index) * con.CELLSIZE, (1 + col_index) * con.CELLSIZE, con.CELLSIZE, con.CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, color_map[board[row_index][col_index]], tileRect)

if __name__ == '__main__':
    main()