import sys, os
from datetime import datetime, timedelta
from os.path import join
from hashlib import sha1
from time import time

class Intersect:
    def __init__(self, inputFolder, outputFolder, frameLength, candidateSizeThreshold = 2, candidateDurationThreshold = 3): # candidateDurationThreshold unit: frame
        self.inputFolder = inputFolder
        self.outputFolder = outputFolder
        self.candidateSizeThreshold = candidateSizeThreshold
        self.candidateDurationThreshold = candidateDurationThreshold
        self.frameLength = frameLength


    def expire(self, duration, startTime, currentTime) :
                startTimeNonStr = datetime.strptime(startTime, "%H%M")
                if currentTime - startTimeNonStr > timedelta(seconds = duration * 60):
                    return False
                else:
                    return True

    def intersect(self):
        #filename of the first file
        filenameSeq = []
        for i in range(self.frameLength):
            filenameSeq.append(str(i))

        candidates = []
        for filename in filenameSeq:
            print filename
            print len(candidates)
            if not os.path.isdir(join(self.inputFolder, filename)):
                with open(join(self.inputFolder, filename), 'r') as f:
                    clusters = []

                    #loading file
                    for lines in f:
                        terms = lines.strip().split(',')[:-1]
                        clusters.append(set(terms))

                    #intersection between candidates and current clusters
                    interResult = []
                    for currentCluster in clusters:
                        for cluster, duration in candidates:
                            inter = cluster & currentCluster
                            if len(inter) >= self.candidateSizeThreshold:
                                interResult.append((inter, duration + 1))

                    for currentCluster in clusters:
                        if len(interResult) > 0 and currentCluster in zip(*interResult)[0]:
                            continue
                        interResult.append((currentCluster, 1))
                    candidates = interResult

                    #candidates = filter(lambda clusterDurationStartTime: expire(clusterDurationStartTime[1], clusterDurationStartTime[2], datetime.strptime(filename, "%H%M")), candidates)
                    with open(join(self.outputFolder, filename), 'w') as rec:
                        for cluster, duration in candidates:
                            if len(cluster) >= self.candidateSizeThreshold and duration >= self.candidateDurationThreshold:
                                for uid in cluster:
                                    rec.write(uid + ',')
                                rec.write(str(duration) + '\n')

