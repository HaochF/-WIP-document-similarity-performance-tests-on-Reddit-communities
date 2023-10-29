import ndjson
import collections
import plot
from sklearn.manifold import TSNE
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import json
from sklearn.cluster import KMeans





f = open("subreddit-names-in-tsne-order", "r")
tsne_names = f.read()[1:len(f.read())-1]
tsne_names = tsne_names.replace('"', ' ')
tsne_names = tsne_names.replace(',', ' ')
tsne_names = tsne_names.split(' ')

tsne_names = list(filter(('').__ne__, tsne_names))

f2 = open("tsne-results", "r")
coords = f2.read().replace('\n', ' ')
coords = coords.split(' ')
del coords[len(coords)-1]
coords = [float(x) for x in coords]

coords = [(coords[i],coords[i+1]) for i in range(0,len(coords),2)]


Xtsne = [(x[0]) for x in coords]
Ytsne = [(x[1]) for x in coords]

plt.scatter(Xtsne, Ytsne)



for i, label in enumerate(tsne_names):
    plt.annotate(label, (Xtsne[i], Ytsne[i]))

plt.show()


