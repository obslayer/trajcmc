import sys, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread

patternPath = '/home/wang/workplace/zyed/pattern/'
rawDataPath = '/home/wang/workplace/zyed/data/'
imageOutputPath = './patternImg/'

def getCoordinate(filename, lineNum):    #the filename here is UID
    f = open(rawDataPath + "P%(filename)s.csv" % locals(), 'r')
    coordinate = []
    for num, line in enumerate(f):
        if(lineNum == num):
            terms = line.strip().split(',')
            coordinate = [float(terms[0]), float(terms[1])]
    f.close()
    return coordinate


def showPattern(filename):
    # loading
    clusters = {}
    with open(patternPath + filename) as f:
        for line in f:
            terms = line.strip().split(',')

            cluster = []
            for uid in terms[:-1]:
                cluster.append(uid)

            #get distinct clusters
            cid = frozenset(cluster)
            if cid in clusters:
                if clusters[cid] < int(terms[-1]):
                    clusters[cid] = int(terms[-1])
            else:
                clusters[cid] = int(terms[-1])


    colors = plt.cm.Spectral(np.linspace(0, 1, len(clusters)))
    DPI = 96
    fig = plt.figure(figsize=(1920/DPI, 1080/DPI), dpi = DPI)
    ax = fig.add_subplot(111)
    for (cluster, duration), color in zip(clusters.items(), colors):
        #load coordinate
        coordinate = []
        for uid in cluster:
            coordinate.append(getCoordinate(uid, int(filename) ))
        coordinate = np.array(coordinate)
        plt.plot(coordinate[:, 0], coordinate[:, 1], 'o', markerfacecolor = color)
        left, width = coordinate[0][0], 50
        bottom, height = coordinate[0][1], 50
        right = left + width
        top = bottom + height

        #ax.text(0.5*(left+right), 0.5*(bottom+top), str(duration) + ',' + cluster.__iter__().next(),
        #show pattern commend
        ax.text(0.5*(left+right), 0.5*(bottom+top), str(duration),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, color=color,
            transform=ax.transData)

        ax.set_axis_off()


    #show frame number
    ax.text(60, 20, str(filename),
            horizontalalignment='center',
            verticalalignment='top',
            fontsize=15, color='r',
            transform=ax.transData)



    backgroud = imread("/home/wang/data/FrameRenamed/" + filename)
    plt.imshow(backgroud, zorder = 0)
    plt.savefig(imageOutputPath + filename,  facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1,
            frameon=None)
    #plt.show()
    
    plt.close('all')


# get arguments
argvs = sys.argv
#filename = argvs[1]   #the filename here has a semantic meaning of time
for filename in range(906):
    showPattern(str(filename))
