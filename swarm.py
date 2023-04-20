from random import randint, sample
from vacuum import *
from Site import *
import enums.constants

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

    def __init__(self, agentCount, siteCount, sitePattern, target):
        self.generate_agents(agentCount)
        self.generate_sites(siteCount, sitePattern, target)

    def generate_agents(self, agentCount):
        for i in range(agentCount):
            self.agents.append(vacuum([randint(0, 20), randint(0, 20)], enums.constants.BLACK))

    def generate_sites(self, siteCount, sitePattern, target):
        self.sites.append(Site(sitePattern, target))
        for i in range(siteCount - 1):
            # Generate 3 random numbers that sum to 100
            dividers = sorted(sample(range(1, 100), 2))
            feat1, feat2, feat3 = (a - b for a, b in zip(dividers + [100], [0] + dividers))
            self.sites.append(Site(sitePattern, [feat1, feat2, feat3]))

    def simulate(self, timesteps):
        for site in self.sites:
            # TODO the agents will need to be given the new site and new starting coordinates here
            for step in range(timesteps):
                for agent in self.agents:
                    agent.random_move()

    def do_dowdall_vote(self):
        voteTotals = [0] * len(self.sites)
        for agent in self.agents:
            vote = agent.get_vote()
            for i in range(len(vote)):
                voteTotals[vote[i]] += 1 / (i + 1)

        return voteTotals

    def do_borda_vote(self):
        voteTotals = [0] * len(self.sites)
        for agent in self.agents:
            vote = agent.get_vote()
            for i in range(len(vote)):
                voteTotals[vote[i]] += (len(self.sites))

        return voteTotals