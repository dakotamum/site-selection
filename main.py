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
    do_timestep(1, 100, 1, 10)
    #do_agents(1, 100, 1, 100)
    #do_sites(10, 100, 1, 100)
    return False

def do_sites(lowerBound, upperBound, step, trials):
    print('Generating site data')
    dowdallRecord = []
    bordaRecord = []
    timesteps = []

    i = lowerBound
    while i <= upperBound:
        print("Working on site num %s" % i)
        timesteps.append(i)
        dowdallCorrect = 0
        bordaCorrect = 0
        for j in range(trials):
            swarm = Swarm(agentCount=CONFIG['num_drones'], siteCount=i, sitePattern=0, siteType='Random')
            swarm.simulate(CONFIG['num_timesteps'], CONFIG)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals[0]:
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals[0]:
                bordaCorrect += 1
        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Sites')
    plt.xlabel('Sites')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Sites.png')

def do_agents(lowerBound, upperBound, step, trials):
    print('Generating agent data')
    dowdallRecord = []
    bordaRecord = []
    timesteps = []

    i = lowerBound
    while i <= upperBound:
        print("Working on agent num %s" % i)
        timesteps.append(i)
        dowdallCorrect = 0
        bordaCorrect = 0
        for j in range(trials):
            swarm = Swarm(agentCount=i, siteCount=CONFIG['num_sites'], sitePattern=0, siteType='Base')
            swarm.simulate(CONFIG['num_timesteps'], CONFIG)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals[0]:
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals[0]:
                bordaCorrect += 1
        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Agents')
    plt.xlabel('Agents')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Agents.png')

def do_timestep(lowerBound, upperBound, step, trials):
    print('Generating timestep data')
    dowdallRecord = []
    bordaRecord = []
    timesteps = []

    i = lowerBound
    while i <= upperBound:
        print("Working on timestep %s" % i)
        timesteps.append(i)
        dowdallCorrect = 0
        bordaCorrect = 0
        for j in range(trials):
            swarm = Swarm(agentCount=CONFIG['num_drones'], siteCount=CONFIG['num_sites'], sitePattern=0,
                          siteType='Base')
            swarm.simulate(i, CONFIG)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals[0]:
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals[0]:
                bordaCorrect += 1
        dowdallRecord.append(dowdallCorrect / trials)
        bordaRecord.append(bordaCorrect / trials)
        i += step

    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    plt.legend()
    plt.clf()
    plt.title('Swarm Accuracy vs Number of Simulated Timesteps')
    plt.xlabel('Timesteps')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Timesteps.png')


if __name__ == '__main__':
    main()