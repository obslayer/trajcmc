import numpy as np
import sys, os

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from os.path import join


def dbscan(inputFolder, outputFolder):
    for filename in os.listdir(inputFolder):
        if not os.path.isdir(join(inputFolder, filename)):
            print filename
            with open(join(inputFolder, filename), 'r') as f:
                out = open(join(outputFolder, filename), 'w')
                UIDs = []
                coordinates = []
                for lines in f:
                    terms = lines.strip().split(',')
                    uid = int(terms[0])
                    x = float(terms[1])
                    y = float(terms[2])
                    UIDs.append(uid)
                    coordinates.append([x, y])
                UIDs = np.array(UIDs)
                coordinates = np.array(coordinates)
                #data = StandardScaler().fit_transform(data)

                db = DBSCAN(eps=54, min_samples=2).fit(coordinates)
                core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
                core_samples_mask[db.core_sample_indices_] = True
                labels = db.labels_

                print len(labels)
                n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
                print('Estimated number of clusters: %d' % n_clusters_)
                unique_labels = set(labels)
                for k in unique_labels:
                    if k != -1:
                        class_member_mask = (labels == k)
                        uidCluster = UIDs[class_member_mask]
                        for uid in uidCluster:
                            out.write(str(uid) + ',')
                    out.write('\n')
                out.close()
