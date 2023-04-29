# Robot swarm site selection project

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import json

import Swarm
from Drone import *
from Site import *
from Swarm import *
from pygame.locals import *

import sys
import enums.constants as con
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) <= 1:
        print('Syntax is main.py [independent variable] [lower bound] [upper bound] [step size] [number of trials]')
        print('Independent vairables are: \'timestep\', \'agent\', and \'site\'')
    else:
        while runGame(sys.argv):
            """"""

def runGame(args):
    if args[1] == 'timestep':
        do_timestep(int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    elif args[1] == 'agent':
        do_agents(int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    elif args[1] == 'site':
        do_sites(int(args[2]), int(args[3]), int(args[4]), int(args[5]))
    elif args[1] == 'distribution':
        do_distributions(int(args[2]))
    else:
        print("Invalid Syntax")
    return False

# Compare between random and block 
def do_distributions(trials):
    dowdallAccuracy = {'random': 0, 'block': 0}
    bordaAccuracy = {'random': 0, 'block': 0}
    stvAccuracy = {'random': 0, 'block': 0}

    dowdallCorrect = {'random': 0, 'block': 0}
    bordaCorrect = {'random': 0, 'block': 0}
    stvCorrect = {'random': 0, 'block': 0}

    for type_index, type in enumerate(['random', 'block']):
        for _ in range(trials):
            swarm = Swarm(agentCount=con.NUM_DRONES, siteCount=con.NUM_SITES, sitePattern=type_index, siteType='Base')
            swarm.simulate(con.NUM_TIMESTEPS)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals.index(max(dowdall_totals)):
                dowdallCorrect[type] += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals.index(max(borda_totals)):
                bordaCorrect[type] += 1
            
            stv_totals = swarm.do_stv_vote()
            if swarm.targetIndex == stv_totals.index(max(stv_totals)):
                stvCorrect[type] += 1

        dowdallAccuracy[type] = (dowdallCorrect[type] / trials) * 100
        bordaAccuracy[type] = (bordaCorrect[type] / trials) * 100
        stvAccuracy[type] = (stvCorrect[type] / trials) * 100

        # Bar chart setup
    n_groups = 2
    bar_width = 0.25
    opacity = 0.8

    # X-axis labels
    labels = ["Random", "Block"]

    # X-axis positions for each group of bars
    index = np.arange(n_groups)

    # Create bar chart
    fig, ax = plt.subplots()

    rects1 = ax.bar(index, [dowdallAccuracy["random"], dowdallAccuracy["block"]], bar_width,
                    alpha=opacity, color='b', label='Dowdall')

    rects2 = ax.bar(index + bar_width, [bordaAccuracy["random"], bordaAccuracy["block"]], bar_width,
                    alpha=opacity, color='r', label='Borda')

    rects3 = ax.bar(index + 2 * bar_width, [stvAccuracy["random"], stvAccuracy["block"]], bar_width,
                    alpha=opacity, color='g', label='STV')

    # Add labels, title, and legend
    ax.set_xlabel('Type')
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Accuracy by Type and Method')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(labels)
    ax.legend()

    # Display the bar chart
    plt.savefig('Distributions.png')
    


def do_sites(lowerBound, upperBound, step, trials):
    print('Generating site data')
    dowdallRecord = []
    bordaRecord = []
    stvRecord = []
    timesteps = []

    i = lowerBound
    while i <= upperBound:
        print("Working on site num %s" % i)
        timesteps.append(i)
        dowdallCorrect = 0
        bordaCorrect = 0
        stvCorrect = 0

        for j in range(trials):
            swarm = Swarm(agentCount=con.NUM_DRONES, siteCount=i, sitePattern=0, siteType='Random')
            swarm.simulate(con.NUM_TIMESTEPS)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals.index(max(dowdall_totals)):
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals.index(max(borda_totals)):
                bordaCorrect += 1
            
            stv_totals = swarm.do_stv_vote()
            if swarm.targetIndex == stv_totals.index(max(stv_totals)):
                stvCorrect += 1

        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        stvRecord.append((stvCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda', alpha=0.25, color='blue')
    plt.plot(timesteps, dowdallRecord, label='Dowdall', alpha=0.25, color='red')
    plt.plot(timesteps, stvRecord, label="STV", alpha=0.25, color='green')
    # Add Borda trendline
    zb = np.polyfit(timesteps, bordaRecord, 4)
    pb = np.poly1d(zb)
    plt.plot(timesteps, pb(timesteps), label='Borda Trendline', color='blue')
    # Add Dowdall trendline
    zd = np.polyfit(timesteps, dowdallRecord, 4)
    pd = np.poly1d(zd)
    plt.plot(timesteps, pd(timesteps), label='Dowdall Trendline', color='red')
    # Add STV trendline
    sb = np.polyfit(timesteps, stvRecord, 4)
    sd = np.poly1d(sb)
    plt.plot(timesteps, sd(timesteps), label='STV Trendline', color='green')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Agents')
    plt.xlabel('Sites')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Sites.png')

def do_agents(lowerBound, upperBound, step, trials):
    print('Generating agent data')
    dowdallRecord = []
    bordaRecord = []
    stvRecord = []
    timesteps = []

    i = lowerBound
    while i <= upperBound:
        print("Working on agent num %s" % i)
        timesteps.append(i)
        dowdallCorrect = 0
        bordaCorrect = 0
        stvCorrect = 0

        for j in range(trials):
            swarm = Swarm(agentCount=i, siteCount=con.NUM_SITES, sitePattern=0, siteType='Base')
            swarm.simulate(con.NUM_TIMESTEPS)

            dowdall_totals = swarm.do_dowdall_vote()
            if swarm.targetIndex == dowdall_totals.index(max(dowdall_totals)):
                dowdallCorrect += 1

            borda_totals = swarm.do_borda_vote()
            if swarm.targetIndex == borda_totals.index(max(borda_totals)):
                bordaCorrect += 1

            stv_totals = swarm.do_stv_vote()
            if swarm.targetIndex == stv_totals.index(max(stv_totals)):
                stvCorrect += 1
        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        stvRecord.append((stvCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda', alpha=0.25, color='blue')
    plt.plot(timesteps, dowdallRecord, label='Dowdall', alpha=0.25, color='red')
    plt.plot(timesteps, stvRecord, label='STV', alpha=0.25, color='green')
    
    # Add Borda trendline
    zb = np.polyfit(timesteps, bordaRecord, 3)
    pb = np.poly1d(zb)
    plt.plot(timesteps, pb(timesteps), label='Borda Trendline', color='blue')

    # Add Dowdall trendline
    zd = np.polyfit(timesteps, dowdallRecord, 3)
    pd = np.poly1d(zd)
    plt.plot(timesteps, pd(timesteps), label='Dowdall Trendline', color='red')

    # Add STV trendline
    zs = np.polyfit(timesteps, stvRecord, 3)
    ps = np.poly1d(zs)
    plt.plot(timesteps, ps(timesteps), label='STV Trendline', color='green')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Agents')
    plt.xlabel('Number of Agents')
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
            
            stv_totals = swarm.do_stv_vote()
            if swarm.targetIndex == stv_totals.index(max(stv_totals)):
                stvCorrect += 1

        dowdallRecord.append((dowdallCorrect / trials) * 100)
        bordaRecord.append((bordaCorrect / trials) * 100)
        stvRecord.append((stvCorrect / trials) * 100)
        i += step

    plt.clf()
    plt.plot(timesteps, bordaRecord, label='Borda')
    plt.plot(timesteps, dowdallRecord, label='Dowdall')
    plt.plot(timesteps, stvRecord, label='STV')
    
    # Add Borda trendline
    zb = np.polyfit(timesteps, bordaRecord, 2)
    pb = np.poly1d(zb)
    plt.plot(timesteps, pb(timesteps), label='Borda Trendline')

    # Add Dowdall trendline
    zd = np.polyfit(timesteps, dowdallRecord, 2)
    pd = np.poly1d(zd)
    plt.plot(timesteps, pd(timesteps), label='Dowdall Trendline')

    # Add STV trendline
    zs = np.polyfit(timesteps, stvRecord, 2)
    ps = np.poly1d(zs)
    plt.plot(timesteps, ps(timesteps), label='STV Trendline')
    plt.legend()
    plt.title('Swarm Accuracy vs Number of Simulated Timesteps')
    plt.xlabel('Timesteps')
    plt.ylabel('Accuracy (%)')
    plt.savefig('Timesteps.png')


if __name__ == '__main__':
    main()