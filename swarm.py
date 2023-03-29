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

    def __init__(self, agentCount, siteCount, sitePattern, siteFeatures):
        self.generate_agents(agentCount)
        self.generate_sites(siteCount, sitePattern, siteFeatures)

    def generate_agents(self, agentCount):
        pass

    def generate_sites(self, siteCount, sitePattern, siteFeatures):
        pass

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