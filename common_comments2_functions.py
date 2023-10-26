import ndjson
import collections
import plot
from sklearn.manifold import TSNE
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import json
import math

def distance(word_counts_A, word_counts_B):
  overlapping = set(word_counts_A.keys()).union(set(word_counts_B.keys()))
  sum = 0
  for word in overlapping:
    if word not in word_counts_A:
      sum += word_counts_B[word]**2
      continue
    if word not in word_counts_B:
      sum += word_counts_A[word]**2
      continue
    sum += (word_counts_A[word] - word_counts_B[word])**2

  return sum**0.5

def cosine_dis(word_counts_A, word_counts_B):
  overlapping = set(word_counts_A.keys()).union(set(word_counts_B.keys()))
  sumdot = 0
  for word in overlapping:
    if word not in word_counts_A:
      continue
    if word not in word_counts_B:
      continue
    sumdot += word_counts_A[word]*word_counts_B[word]
  
  abs_A = 0
  for word in word_counts_A.keys():
    abs_A += word_counts_A[word]**2
  abs_A = math.sqrt(abs_A)

  abs_B = 0
  for word in word_counts_B.keys():
    abs_B += word_counts_B[word]**2
  abs_B = math.sqrt(abs_B)

  return (1-sumdot/(abs_A*abs_B))

def get_farthest_from_weights(SubListMulti, subredditWordCounts, SubsToProcess):
  maxnum = -1.1
  maxname = ''
  totalWeight = 0.0


  for subToCompare, weight in SubListMulti.items():
    totalWeight += weight

  for subreddit in SubsToProcess:
    sum = 0.0
    for subToCompare, weight in SubListMulti.items():
      sum += distance(subredditWordCounts[subToCompare],
                      subredditWordCounts[subreddit]) * weight
    if maxnum < sum:
      maxnum = sum
      maxname = subreddit

  maxnum /= totalWeight

  #print(maxname, " has a distance of: ", maxnum, " from selected subreddits")

  return maxname