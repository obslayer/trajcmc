import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pathos.multiprocessing as mp
from multiprocessing import Pool
from scipy.misc import imread
from os.path import join


class RenderPattern:
    def __init__(self, patternPath, rawDataPath, imageOutputPath, frameImagePath, frameLength):
        self.patternPath = patternPath
        self.rawDataPath = rawDataPath
        self.imageOutputPath = imageOutputPath
        self.frameImagePath = frameImagePath
        self.frameLength = frameLength


    #get a signle coordinate by filename and offset
    def getCoordinate(self, filename, lineNum):    #the filename here is UID, T: str, int
        f = open(join(self.rawDataPath, "P%(filename)s.csv" % locals()), 'r')
        coordinate = []
        for num, line in enumerate(f):
            if(lineNum == num):
                terms = line.strip().split(',')
                coordinate = [float(terms[0]), float(terms[1])]
        f.close()
        return coordinate


    #get a sequence of coordinates by filename, offset and duration
    def getTrajSegment(self, filename, offset, duration):  #the filename here is UID, T: str, int, int
        f = open(join(self.rawDataPath, "P%(filename)s.csv" % locals()), 'r')
        coordinates = []
        for num, line in enumerate(f):
            if num > offset  and num <= offset + duration :
                terms = line.strip().split(',')
                coordinates.append([float(terms[0]), float(terms[1])])
        f.close()
        return coordinates

    # render one frame
    def render(self, filename):
        # loading
        clusters = {}

        with open(join(self.patternPath, filename)) as f:
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
        displayDPI = 96
        fig = plt.figure(figsize=(1920/displayDPI, 1080/displayDPI), dpi=displayDPI)
        ax = fig.add_subplot(111)
        for (cluster, duration), color in zip(clusters.items(), colors):
            # load coordinate
            coordinate = []
            for uid in cluster:
                coordinate.append(self.getTrajSegment(uid, int(filename) - duration, duration))
            coordinate = np.array(coordinate)

            # plot the points
            try:
                plt.plot(coordinate[:, -1, 0], coordinate[:, -1, 1], 'o', markerfacecolor=color)
            except:
                print coordinate
                print duration
            for traj in coordinate:
                plt.plot(traj[:, 0], traj[:, -1], '-', color = color)
            left, width = coordinate[0, -1, 0], 50
            bottom, height = coordinate[0, -1, 1], 50
            right = left + width
            top = bottom + height

            # ax.text(0.5*(left+right), 0.5*(bottom+top), str(duration) + ',' + cluster.__iter__().next(),
            # show pattern commend
            ax.text(0.5*(left+right), 0.5*(bottom+top), str(duration), horizontalalignment='center', verticalalignment='center', fontsize=20, color=color, transform=ax.transData)
            ax.set_axis_off()


        # show frame number
        ax.text(60, 20, str(filename),
                horizontalalignment='center',
                verticalalignment='top',
                fontsize=15, color='r',
                transform=ax.transData)



        backgroud = imread(join(self.frameImagePath, filename))
        plt.imshow(backgroud, zorder = 0)
        fig.tight_layout()
        plt.savefig(join(self.imageOutputPath, filename),  facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches=None, pad_inches=0,
                frameon=None)
        # plt.show()
        plt.close('all')

    def renderPattern(self):
        pool = mp.ProcessingPool(6)
        pool.map(self.render, [str(x) for x in range(self.frameLength)])
