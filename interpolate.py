import os,scipy,sys
import numpy as np
from os.path import join
from multiprocessing import Pool


def takeSnapshot(inputFolder, outputFolder):
    for filename in os.listdir(inputFolder):
        if not os.path.isdir(join(inputFolder, filename)):
            with open(join(inputFolder, filename), 'r') as f:
                timeIndex = 0
                for line in f:
                    with open(join(outputFolder, str(timeIndex)), 'a') as g:
                        if(line.strip() != "0,0"):
                            #correct the filename.      P14723.csv -> 14723
                            #output format is UID,x,y
                            g.write(filename[1:-4] + ',' + line)
                    timeIndex = timeIndex + 1


def interpolate(filename):
    with open(rawTrajPath + filename, 'r') as f:
        traj = []

        #loading
        for line in f:
            terms = line.strip().split(",")
            traj.append([float(terms[0]),float(terms[1])])

        #probe interpolation points
        startIndex = 0
        for x, y in traj:
            if x == 0.0 and y == 0.0:
                startIndex = startIndex + 1
            else:
                break


        zeroFlag = False
        prevZeroFlag = False
        currentOffset = 0

        interpStart = []
        interpEnd = []
        for x,y in traj[startIndex:]:
            if x == 0.0 and y == 0.0:
                zeroFlag=True
            else:
                zeroFlag=False

            if zeroFlag != prevZeroFlag:
                if zeroFlag == True:
                    interpStart.append(currentOffset)
                else:
                    interpEnd.append(currentOffset)
            prevZeroFlag = zeroFlag
            currentOffset = currentOffset + 1


        interpStart = np.array(interpStart)
        interpEnd = np.array(interpEnd)

        interpStart = interpStart + startIndex
        interpEnd = interpEnd + startIndex

        
        #do the interpolation
        for start, end in zip(interpStart, interpEnd):
            deltaX = np.linspace(traj[start - 1][0], traj[end][0], end - start + 2)
            deltaY = np.linspace(traj[start - 1][1], traj[end][1], end - start + 2)
            delta = np.array(zip(deltaX, deltaY))
            traj[start:end] += delta[1:-1]

    #output
    with open(interpolatedDataPath + filename, 'w') as f:
        for x,y in traj:
            f.write("%f,%f\n" % (x,y))
            

