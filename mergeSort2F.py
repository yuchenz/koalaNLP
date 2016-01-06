#!/usr/bin/python2.7

# merged two sorted files into one sorted file 

import codecs, sys
import pdb

def sortLines(filename1, filename2, filename3):
	f = codecs.open("/dev/shm/"+filename3+'.sorted', 'w', 'utf-8')
	f1 = codecs.open(filename1, 'r', 'utf-8')
	f2 = codecs.open(filename2, 'r', 'utf-8')
	
	line1 = f1.next()
	line2 = f2.next()
	flag = 0
	while True: 
		if line1 > line2:
			try:
				f.write(line2)
				line2 = f2.next()
			except StopIteration:
				flag = 2
				break
		else:
			try:
				f.write(line1)
				line1 = f1.next()
			except StopIteration:
				flag = 1
				break
	
	if flag == 2:
		f.write(line1)
		while True: 
			try:
				f.write(f1.next())
			except StopIteration:
				break
	elif flag == 1:	
		f.write(line2)
		while True:
			try:
				f.write(f2.next())
			except StopIteration:
				break
	
	f.close()

if __name__ == "__main__":
	sortLines(sys.argv[1], sys.argv[2], sys.argv[3])
