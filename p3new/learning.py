import mountaincar
from Tilecoder import numTilings, numTiles, tilecode
from pylab import *  # includes numpy

numRuns = 5
n = numTiles * 3



def learn(alpha=.1 / numTilings, epsilon=0, numEpisodes=200):
    theta1 = -0.001 * rand(n)
    theta2 = -0.001 * rand(n)
    returnSum = 0.0
    Qs1 = np.zeros(3)
    Qs2 = np.zeros(3)
    steps_list = np.zeros(numEpisodes)
    return_list = np.zeros(numEpisodes)
    for episodeNum in range(numEpisodes):
        G = 0
        s = mountaincar.init()
        step = 0
        while s != None:
            step +=1
            t1 = [-1] * numTilings
            t1 =tilecode(s[0], s[1], t1)
            for i in range(3):
                Qs1[i] = qvalues(theta1, i, t1)
                Qs2[i] = qvalues(theta2, i, t1)

            greedy = np.random.random()
            if greedy < epsilon:
                a = np.random.randint(3)
            else:
                a = np.argmax((Qs1 + Qs2))

            r, ss = mountaincar.sample(s,a)
            G += r
            p = np.random.randint(2)
            if ss == None:
                break
            t2 = [-1] * 4
            t2 = tilecode(ss[0], ss[1], t2)
            if p == 0:
                Q_ss = [ qvalues(theta1,0, t2), qvalues(theta1, 1, t2), qvalues(theta1, 2, t2)] 
                a_ss = np.argmax(Q_ss)
                Q_ss = qvalues(theta2, a_ss,t2)
                for i in t1:
                    theta1[i + a * 324] += alpha * (r + Q_ss - Qs1[a])
            if p == 1:
                Q_ss = [ qvalues(theta2, 0, t2), qvalues(theta2, 1, t2), qvalues(theta2, 2, t2)] 
                a_ss = np.argmax(Q_ss)
                Q_ss = qvalues(theta1, a_ss, t2)
                for i in t1:
                    theta2[i + a *324] += alpha * (r + Q_ss - Qs2[a])
            s = ss
        if p == 0:
            for i in t1:
                theta1[i + a *324] += alpha * (r - Qs1[a])
        if p == 1:
            for i in t1:
                theta2[i + a *324] += alpha * (r - Qs2[a])

        #print("Episode: ", episodeNum, "Steps:", step, "Return: ", G)
        returnSum = returnSum + G
        steps_list[episodeNum] += step
        return_list[episodeNum] += G
    #print("Average return:", returnSum / numEpisodes)
    #writeF(theta1, theta2)
    #writeMy(numEpisodes, return_list, steps_list)
    return returnSum, theta1, theta2


# Additional code here to write average performance data to files for plotting...
def qvalues(theta, a, tileIndices):
    # write your linear function approximator here (5 lines or so)
    sums = 0
    for i in tileIndices:
        sums += theta[i + a *324]
    return sums

def writeMy(numEpisodes, return_list, steps_list):
    fout = open('avgret.dat' ,'w')
    for i in range(numEpisodes):
        fout.write(repr(i) + ' ' + repr(return_list[i]) + ' ' + repr(steps_list[i]))
        fout.write('\n')
    fout.close()

def writeF(theta1, theta2):
    Q1 = np.zeros(3)
    Q2 = np.zeros(3)
    fout = open('value', 'w')
    steps = 50
    tile = [-1] * 4
    for i in range(steps):
        for j in range(steps):
            F = tilecode(-1.2 + i * 1.7 / steps, -0.07 + j * 0.14 / steps, tile)
            for k in range(3):
                Q1[k] = qvalues(theta1, k, F)
                Q2[k] = qvalues(theta2, k, F)
            a = np.argmax((Q1+Q2))
            #height = -max(Qs(F, theta1, theta2))
            height = -max((Q1+Q2))
            fout.write(repr(height) + ' ')
        fout.write('\n')
    fout.close()


if __name__ == '__main__':
    runSum = 0.0
    for run in range(numRuns):
        returnSum, theta1, theta2 = learn()
        runSum += returnSum
    #print("Overall performance: Average sum of return per run:", runSum/numRuns)
