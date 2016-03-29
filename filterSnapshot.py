#this programme can filter 0.0 points in snapshots
import sys, os

snapshotPath = "./snapshot/"
filteredSnapshotPath = "./filteredSnapshot/"
files = os.listdir(snapshotPath)
for filename in files:
    with open(snapshotPath + filename, 'r') as f, open(filteredSnapshotPath + filename, 'w') as g:
        for line in f:
            terms = line.strip().split(',')
            if float(terms[1]) != 0 and float(terms[2]) != 0:
                g.write(line)
        
