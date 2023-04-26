from random import randint, sample
from Drone import *
from Site import *
from main import *
import pygame, sys
import enums.constants as con
from pygame.locals import *
import matplotlib.pyplot as plt

"""
    Class for the swarm containing all the agents.
    Attributes
    ----------
    agents
        List of individual agents

    sites
        List of sites
"""

class Swarm:
    agents = []
    sites = []
    targetIndex = 0

    def __init__(self, agentCount, siteCount, sitePattern, siteType='Base'):
        self.sites = []
        self.agents = []
        self.generate_agents(agentCount)
        if (siteType == 'Random'):
            self.generate_sites(siteCount, sitePattern)
        else:
            self.generate_base_sites(sitePattern)

    def generate_base_sites(self, sitePattern):
        # generate sites
        for val in con.K:
            self.sites.append(Site(sitePattern, [val[0] * 100, val[1] * 100, val[2] * 100]))
        # randomly select a target site
        self.targetIndex = randint(0, len(self.sites) - 1)
    def generate_agents(self, agentCount):
        color_iteration_size = 0 if con.NUM_DRONES < 2 else int(1530 / (con.NUM_DRONES))
        curr_color = 0
        for i in range(con.NUM_DRONES):
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
            curr_color += color_iteration_size
            self.agents.append(Drone([randint(0, 19), randint(0, 19)], color))
        
    def generate_sites(self, siteCount, sitePattern):
        # pick a candidate site from K
        selectedK = randint(0, 35)
        self.targetIndex = 0
        self.sites.append(Site(sitePattern, [con.K[selectedK][0] * 100, con.K[selectedK][1] * 100,
                                             con.K[selectedK][2] * 100]))
        for i in range(siteCount - 1):
            # Generate 3 random numbers that sum to 100
            dividers = sorted(sample(range(1, 100), 2))
            feat1, feat2, feat3 = (a - b for a, b in zip(dividers + [100], [0] + dividers))
            self.sites.append(Site(sitePattern, [feat1, feat2, feat3]))

    def simulate(self, timesteps, CONFIG):
        if CONFIG['headless_mode'] == False:
            pygame.init()
            FPSCLOCK = pygame.time.Clock()
            global DISPLAYSURF
            DISPLAYSURF = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT))
            pygame.display.set_caption('Swarm Site Select Simulation')
        for site in self.sites:
            # TODO the agents will need to be given the new site and new starting coordinates here
            for step in range(timesteps):
                if CONFIG['headless_mode'] == False:
                    DISPLAYSURF.fill(con.WHITE)
                    self.drawTiles(site.board)
                    self.drawGrid()
                    self.drawDrones(self.agents)
                    for event in pygame.event.get(): 
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                    FPSCLOCK.tick(con.FPS)

                for agent in self.agents:
                    row = agent.current_coordinates[0]
                    col = agent.current_coordinates[1]
                    obs = []
                    if site.board[row][col] == 0:
                        obs = [1, 0, 0]
                    elif site.board[row][col] == 1:
                        obs = [0, 1, 0]
                    else: 
                        obs = [0, 0, 1]
                    agent.update_beliefs(con.K, obs)
                    agent.random_move()

            for agent in self.agents:
                agent.current_coordinates = [randint(0, 19), randint(0, 19)]
                agent.stored_beliefs.append(agent.beliefs)
                agent.beliefs = np.full((36, 1), 1/36)


    def do_dowdall_vote(self):
        voteTotals = [0] * len(self.sites)
        for agent in self.agents:
            vote = agent.get_vote(self.targetIndex)
            for i in range(len(vote)):
                voteTotals[vote[i]] += 1 / (i + 1)

        return voteTotals

    def do_borda_vote(self):
        voteTotals = [0] * len(self.sites)
        for agent in self.agents:
            vote = agent.get_vote(self.targetIndex)
            for i in range(len(vote)):
                voteTotals[vote[i]] += (len(self.sites) - i)
        return voteTotals

    def drawDrones(self, drones):
        for drone in drones:
            x = drone.current_coordinates[0] * con.CELLSIZE
            y = drone.current_coordinates[1] * con.CELLSIZE
            
            pygame.draw.circle(DISPLAYSURF, (0, 0, 0), (x + (con.CELLSIZE / 2), y + (con.CELLSIZE / 2)), (con.CELLSIZE / 2))
            pygame.draw.circle(DISPLAYSURF, drone.color, (x + (con.CELLSIZE / 2), y + (con.CELLSIZE / 2)), (con.CELLSIZE / 2) - 2)

    def drawGrid(self):
        for x in range(0, con.WINDOWWIDTH, con.CELLSIZE): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, con.BLACK, (x, 0), (x, con.WINDOWHEIGHT))
        for y in range(0, con.WINDOWHEIGHT, con.CELLSIZE): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, con.BLACK, (0, y), (con.WINDOWWIDTH, y))

    def drawTiles(self, board):
        color_map = {0: con.BLUE, 1: con.GREEN, 2: con.ORANGE}
        for row_index in range(len(board)):
            for col_index in range(len(board[row_index])):
                tileRect = pygame.Rect((row_index) * con.CELLSIZE, (col_index) * con.CELLSIZE, con.CELLSIZE, con.CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, color_map[board[row_index][col_index]], tileRect)
