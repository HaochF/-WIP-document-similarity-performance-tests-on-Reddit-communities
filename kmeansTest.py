import ndjson
import collections
import plot
from sklearn.manifold import TSNE
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import json
import common_comments2_functions
import read_subreddit_data
from sklearn.cluster import KMeans

with open('Dimensionality_data') as file:
    Dimensionality_data = np.loadtxt(file)

with open('subreddit_names_in_tsne_order_copy') as file:
    subredditNamesInOrder = json.load(file)

kmeans = KMeans(n_clusters=10, n_init=100).fit(Dimensionality_data)


ind = 0
for sub in kmeans.labels_:
    print(subredditNamesInOrder[ind], " cluster: ", sub)
    ind +=1

