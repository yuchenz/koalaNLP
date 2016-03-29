
def waMatrix2oneline(waMatrix):
	oneline = ''
	for i in xrange(len(waMatrix)):
		for j in xrange(len(waMatrix[i])):
			if waMatrix[i][j]:
				oneline += str(i)+'-'+str(j)+' '
	return oneline

def oneline2waMatrix(line, srcLen, tgtLen):
	# the numbers in line has start from 0
	line = [[item.split('-')[0].split(','), item.split('-')[1].split(',')] for item in line.split()]

	wa = [[0 for j in xrange(tgtLen)] for i in xrange(srcLen)]

	for item in line:
		for i in item[0]:
			for j in item[1]:
				wa[int(i)][int(j)] = 1
	
	return wa

	
