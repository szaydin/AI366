import blackjack as bj
import numpy as np
from pylab import *

def run(numEpisodes):
    returnSum = 0.0
    for episodeNum in range(numEpisodes):
        G = 0
        s = bj.init()
        r,s = bj.sample(s, np.random.randint(2))
        G = G + r 
        while s != False:
            r,s = bj.sample(s, np.random.randint(2))
            G = G + r     
        print("Episode: ", episodeNum, "Return: ", G)
        returnSum = returnSum + G
    print("Average = ", (returnSum/numEpisodes))
    return returnSum/numEpisodes

run(10000)