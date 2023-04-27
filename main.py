# Robot swarm site selection project

import json
import Swarm
from Drone import *
from Site import *
from Swarm import *
from pygame.locals import *
import matplotlib as plt
import enums.constants as con

def main():
    runGame()

def runGame():
    #do_sites(2, 50, 1, 10)
    do_timestep(1, 100, 1, 10)
    #do_agents(1, 50, 1, 10)
    # return False

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
            swarm = Swarm(agentCount=con.NUM_DRONES, siteCount=i, sitePattern=0, siteType='Random')
            swarm.simulate(con.NUM_TIMESTEPS)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals.index(max(dowdall_totals)):
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals.index(max(borda_totals)):
                bordaCorrect += 1
        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    # Add Borda trendline
    zb = np.polyfit(timesteps, bordaRecord, 2)
    pb = np.poly1d(zb)
    plt.plot(timesteps, pb(timesteps), label='Borda Trendline')
    # Add Dowdall trendline
    zd = np.polyfit(timesteps, dowdallRecord, 2)
    pd = np.poly1d(zd)
    plt.plot(timesteps, pd(timesteps), label='Dowdall Trendline')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Agents')
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
            swarm = Swarm(agentCount=i, siteCount=con.NUM_SITES, sitePattern=0, siteType='Base')
            swarm.simulate(con.NUM_TIMESTEPS)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals.index(max(dowdall_totals)):
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals.index(max(borda_totals)):
                bordaCorrect += 1
        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    # Add Borda trendline
    zb = np.polyfit(timesteps, bordaRecord, 2)
    pb = np.poly1d(zb)
    plt.plot(timesteps, pb(timesteps), label='Borda Trendline')
    # Add Dowdall trendline
    zd = np.polyfit(timesteps, dowdallRecord, 2)
    pd = np.poly1d(zd)
    plt.plot(timesteps, pd(timesteps), label='Dowdall Trendline')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Agents')
    plt.xlabel('Agents')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Agents.png')

def do_timestep(lowerBound, upperBound, step, trials):
    print('Generating timestep data')
    dowdallRecord = []
    bordaRecord = []
    stvRecord = []
    timesteps = []

    i = lowerBound
    while i <= upperBound:
        print("Working on timestep %s" % i)
        timesteps.append(i)
        dowdallCorrect = 0
        bordaCorrect = 0
        stvCorrect = 0
        for j in range(trials):
            swarm = Swarm(agentCount=con.NUM_DRONES, siteCount=con.NUM_SITES, sitePattern=0,
                          siteType='Base')
            swarm.simulate(i)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals.index(max(dowdall_totals)):
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals.index(max(borda_totals)):
                bordaCorrect += 1
            
            stv_totals = swarm.do_borda_vote()
            if swarm.targetIndex == stv_totals:
                stvCorrect += 1

        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        stvRecord.append((stvCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    plt.plot(timesteps, dowdallRecord, label='STV')
    # Add Borda trendline
    zb = np.polyfit(timesteps, bordaRecord, 2)
    pb = np.poly1d(zb)
    plt.plot(timesteps, pb(timesteps), label='Borda Trendline')
    # Add Dowdall trendline
    zd = np.polyfit(timesteps, dowdallRecord, 2)
    pd = np.poly1d(zd)
    plt.plot(timesteps, pd(timesteps), label='Dowdall Trendline')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Simulated Timesteps')
    plt.xlabel('Timesteps')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Timesteps.png')


if __name__ == '__main__':
    main()