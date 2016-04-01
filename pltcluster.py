import numpy as np
import sys, os
from scipy.misc import imread
from sklearn.cluster import DBSCAN

argvs = sys.argv
frame = argvs[1]

#loading
X = []
f = open("/home/wang/workplace/zyed/snapshot/" + str(frame), 'r')
for lines in f:
    terms = lines.strip().split(',')
    X.append([float(terms[1]), float(terms[2])])
f.close()
print len(X)

# X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
#                             random_state=0)

#X = StandardScaler().fit_transform(X)
X = np.array(X)

r = 54
db = DBSCAN(eps=r, min_samples=2).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=7)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=3)


    plt.title('Estimated number of clusters: %d rad: %f' % (n_clusters_, r))
background = imread("/home/wang/data/FrameRenamed/" + str(frame))
plt.imshow(background, zorder = 0)
plt.show()
