import ndjson
import collections
import plot
from sklearn.manifold import TSNE
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import json
import common_comments2_functions
import math

with open('values_cosine') as json_file:
    distances_euclid = [0]
    for line in json_file:
        distances_euclid.append(float(line))

    distances_euclid = distances_euclid[1:]
    distances_euclid.sort()
    mid = len(distances_euclid) // 2
    res = (distances_euclid[mid] + distances_euclid[~mid]) / 2
    print(res)


with open('values_euclid') as file:
    distances_euclid = [0]
    for line in file:
        distances_euclid.append(float(line))


    distances_euclid = distances_euclid[1:]
    distances_euclid.sort()
    mid = len(distances_euclid) // 2
    res = (distances_euclid[mid] + distances_euclid[~mid]) / 2
    print(res)

with open('subreddit-word-counts') as json_file1:
    subredditWordCounts = json.load(json_file1)
    print(subredditWordCounts['usa'].keys())
