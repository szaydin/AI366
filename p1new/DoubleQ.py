import blackjack as bj
from pylab import *
import numpy as np

gamma = 1
epsilon = 0.01
alpha = 0.001
numberofepisodes = 1000000

Q1 = 0.0001*rand(181,2) # NumPy array of correct size
Q2 = 0.0001*rand(181,2) # NumPy array of correct size
Q1[-1,0]=Q1[-1,1]=0
Q2[-1,0]=Q2[-1,1]=0

def actprob(e,s):
	greedy = np.random.random()
	if greedy < epsilon:
		return np.random.randint(2)
	else:
		TQ = Q1 + Q2
		return np.argmax(TQ[s])
        
def learn(alpha, eps, numTrainingEpisodes):
	returnSum = 0.0
	for episodeNum in range(numTrainingEpisodes):
		G = 0
		s = bj.init() # Fill in Q1 and Q2
		while True:
			a = actprob(epsilon,s)
			r,ss=bj.sample(s,a)
			G = G + r
			p = np.random.randint(0,1)
			if ss == False:
				break
			if p == 0:
				Q1[s,a]=Q1[s,a]+alpha*(r + (gamma * Q2[ss,np.argmax(Q1[ss, :])]) - Q1[s,a])
			if p == 1:
				Q2[s,a]=Q2[s,a]+alpha*(r + (gamma * Q1[ss,np.argmax(Q2[ss, :])]) - Q2[s,a])
			s = ss
		if p == 0:
			Q1[s,a]=Q1[s,a]+alpha*(r - Q1[s,a]) 
		if p == 1:
			Q2[s,a]=Q2[s,a]+alpha*(r - Q2[s,a])
       
		#print("Episode: ", episodeNum, "Return: ", G)
		returnSum = returnSum + G
		#if episodeNum % 10000 == 0 and episodeNum != 0:
			#print("Average return so far: ", returnSum/episodeNum)


def learnedPolicy(s):
	TQ = Q1[s] + Q2[s]
	return np.argmax(TQ)


def evaluate(numEvaluationEpisodes):
	returnSum = 0.0
	for episodeNum in range(numEvaluationEpisodes):
		G = 0
		s = bj.init()
		r, s = bj.sample(s, learnedPolicy(s))
		G +=r
		while s != False:
			r, s = bj.sample(s, learnedPolicy(s))   
			G +=r    
        # Use deterministic policy from Q1 and Q2 to run a number of
        # episodes without updates. Return average return of episodes.
		returnSum = returnSum + G
	return returnSum / numEvaluationEpisodes 


learn(alpha, epsilon, numberofepisodes)
evaluate(numberofepisodes)
#bj.printPolicy(learnedPolicy)
#bj.printPolicyToFile(learnedPolicy)
