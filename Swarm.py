from random import randint, sample
from Drone import *
from Site import *
from main import *

from collections import defaultdict
from typing import List
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
        base_features = [con.K[selectedK][i] * 100 for i in range(0,3)]
        self.sites.append(Site(sitePattern, base_features))

        for i in range(siteCount - 1):
            # Generate 3 random numbers that sum to 100, with a regular variance pattern between features
            # Get a variance value that won't make a feature go over 100%
            maxFeatValue = max(base_features)
            max_variance = 100 - maxFeatValue
            variance = con.FEATURE_RATIO_VARIANCE
            if variance > max_variance:
                variance = max_variance - 1
            feat1 = np.NAN
            feat2 = np.NaN
            feat3 = np.NaN
            feature_choice = randint(1,2)
            if i % 3 == 0:
                feat1 = base_features[0] + variance
                feat2 = base_features[1] - variance if feature_choice == 0 else base_features[1]
                feat3 = base_features[2] if feature_choice == 0 else base_features[2] - variance
            elif i % 3 == 1:
                feat1 = base_features[0] - variance if feature_choice == 0 else base_features[0]
                feat2 = base_features[1] + variance
                feat3 = base_features[2] if feature_choice == 0 else base_features[2] - variance
            elif i % 3 == 2:
                feat1 = base_features[0] - variance if feature_choice == 0 else base_features[0]
                feat2 = base_features[1] if feature_choice == 0 else base_features[1] - variance
                feat3 = base_features[2] + variance
            dividers = sorted(sample(range(1, 100), 2))
            feat1, feat2, feat3 = (a - b for a, b in zip(dividers + [100], [0] + dividers))
            #print(f"Feature1: {int(feat1)}")
            #print(f"Feature2: {int(feat2)}")
            #print(f"Feature3: {int(feat3)}")
            self.sites.append(Site(sitePattern, [int(feat1), int(feat2), int(feat3)]))

    def simulate(self, timesteps):
        if con.HEADLESS_MODE == False:
            pygame.init()
            FPSCLOCK = pygame.time.Clock()
            global DISPLAYSURF
            DISPLAYSURF = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT))
            pygame.display.set_caption('Swarm Site Select Simulation')
        for site in self.sites:
            # TODO the agents will need to be given the new site and new starting coordinates here
            for step in range(timesteps):
                if con.HEADLESS_MODE == False:
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

    def do_stv_vote(self):
        # Get ballots
        ballots = []
        for agent in self.agents:
            ballots.append(agent.get_vote(self.targetIndex))

        # Initialize voteTotals
        voteTotals = [0] * len(self.sites)
    
        # Return a defaultdict showing first chioce data
        def count_first_choices(ballots):
            first_choices = defaultdict(int)
            for ballot in ballots:
                if len(ballot) > 0:
                    first_choices[ballot[0]] += 1
            return first_choices

        # Take candidate out of running and addjust the ballots
        def eliminate_candidate(candidate, ballots):
            new_ballots = []
            for ballot in ballots:
                new_ballot = [c for c in ballot if c != candidate]
                if len(new_ballot) > 0:
                    new_ballots.append(new_ballot)
            return new_ballots

        # Finds the candidates with the most first_choices
        def find_winner(first_choices, num_voters):
            for candidate, votes in first_choices.items():
                if votes > num_voters / 2:
                    return candidate
            return None

        # Finds the candidate with the least votes
        def find_least_votes(first_choices):
            min_votes = float('inf')
            least_voted = None
            for candidate, votes in first_choices.items():
                if votes < min_votes:
                    min_votes = votes
                    least_voted = candidate
            return least_voted

        # Run STV algorithm and update voteTotals
        while True:
            first_choices = count_first_choices(ballots)
            winner = find_winner(first_choices, len(ballots))
            if winner is not None:
                voteTotals[winner] = first_choices[winner]
                break
            least_voted = find_least_votes(first_choices)
            voteTotals[least_voted] = first_choices[least_voted]
            ballots = eliminate_candidate(least_voted, ballots)

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
