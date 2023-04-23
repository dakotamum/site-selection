# Robot swarm site selection project

import json
import Swarm
from Drone import *
from Site import *
from Swarm import *
from pygame.locals import *

def main():
    global CONFIG
    # read config
    f = open ('config.json', "r")
    CONFIG = json.loads(f.read())
    while runGame():
        """"""

def runGame():
    swarm1 = Swarm(agentCount=CONFIG['num_drones'], siteCount=CONFIG['num_sites'], sitePattern=0, target=[33,34,33])
    swarm1.simulate(CONFIG)
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print(swarm1.agents[0].stored_beliefs)
    return False

if __name__ == '__main__':
    main()