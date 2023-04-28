# Swarm Site Selection with Ranked Voting Systems

This program simulates the site selection of a swarm of autonomous agents. Sites are represented as a 20 x 20 grid made up of various color ratios of red, blue, and green tiles. The objective is for the autonomous agents to explore n-number of sites and then select which site contains the prescribed target ratio. The target site is chosen at random at the beginning of each simulation. This program handles the generation of sites and agents and simulates the agents' exploration in each of them for a finite amount of time as specified by the user. The output of the program is the percentage of time the swarm correctly chose the target site out of the total number of simulations ran using both Borda and Dowdall voting mechanisms.

# Running

Syntax is main.py [independent variable] [lower bound] [upper bound] [step size] [number of trials]
Independent variales are:
'timestep': Run simulations equal to the number of trials where the agents are given a variable amount
	of time, starting from lower bound and increasing by step size to upper bound, to explore sites.
	
'agent': Run simulations equal to the number of trials with a variable number of agents, starting from 
	lower bound and increasing by step size to upper bound, exploring sites.
	
'sites': Run simulations equal to the number of trials with a variable number of sites, starting 
	from lower bound and increasing by step size to upper bound, for the agents to explore.
