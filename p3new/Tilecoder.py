numTilings = 4
numTiles = 324

def tilecode(in1, in2, tileIndices):
    # write your tilecoder here (5 lines or so)
	for i in range(0,numTilings):
		index1 = int(((in1 + 1.2) + i * 0.2125/numTilings) * 8/1.7)
		index2 = int(((in2 + 0.07) + i * 0.0175/numTilings) * 8/0.14)
		tileIndices[i] = i*81 + index1 + index2 * 9
	return tileIndices
