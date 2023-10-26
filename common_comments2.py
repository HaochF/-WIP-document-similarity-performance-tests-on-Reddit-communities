





import ndjson
import collections
import plot
from sklearn.manifold import TSNE
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import json
import common_comments2_functions
from sklearn.cluster import KMeans
import string
import pandas as pd
import praw
import json
import re
import time

import os
import requests
from praw.models import MoreComments
from prawcore import NotFound
from prawcore.exceptions import Forbidden





with open('PASSWORD.txt', 'r') as f:
    pw = f.read()

reddit = praw.Reddit(
    client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
    client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
    username = 'tester78780',
    password = pw,
    user_agent = "<ReplyCommentBot1.0>"
)


'''
with addition of new data run:
-this code
-get averages
-testing
'''
remove_subs = True
#RC_2020-01-29
INPUT_FILE = 'shortData'
subreddits_add = [] 
added_sub_size = 200
minSubredditSize = 50
#minSubredditWords = 3000
tsnePerplexity = minSubredditSize/10

def most_common(lst):
  return max(set(lst), key=lst.count)


def least_common(lst):
  return min(set(lst), key=lst.count)


# word_counts_A & B are dictionaries of (normalized) word counts
# e.g. {'the': 0.01, 'and': 0.02}



SubList = []
with open(INPUT_FILE) as f:
  data = ndjson.load(f)
  #print(data[0])
  for i in data:
    SubList.append(i['subreddit'])

AllSubredditsList = []
with open(INPUT_FILE) as f:
  data = ndjson.load(f)
  for i in data:
    AllSubredditsList.append(i['subreddit'])
SubsToProcess = list(set(AllSubredditsList))

sub_counts = []
print('counting... ')
for sub in SubsToProcess:
  c = SubList.count(sub)
  sub_counts.append((sub, c))
sub_counts.append(('_all', len(data)))
# sub_counts = [('_all' 12000), ('politics', 5000), ('gaming', 2000), ...]


def sorting_function(t):
  return -t[1]

print('sorting... ')
sub_counts.sort(key=sorting_function)
sub_counts = dict(sub_counts)
# sub_counts = {'politics': 5000, 'gaming': 2000, ...}

#print(sub_counts)

# remove all subs with <50 posts from SubsToProcess

for (sub, count) in sub_counts.items():
  if count < minSubredditSize:
    SubsToProcess.remove(sub)

temp = len(SubsToProcess)

if remove_subs:
  for sub in SubsToProcess:
    time.sleep(0.3)
    try:
      reddit.subreddits.search_by_name(sub, exact=True)
      try:
        if reddit.subreddit(sub).over18:
          SubsToProcess.remove(sub)
      except Forbidden:
        SubsToProcess.remove(sub)
    except NotFound:
      SubsToProcess.remove(sub)

    
print('deleted ', temp-len(SubsToProcess), ' subreddits')

print("number of subs: ", len(SubsToProcess))

print("large subs:", SubsToProcess)

# {'_all': [...], 'politics': [...], 'gaming': [...], 'reddit.com': [...]}
print('adding... ')
subredditWords = {}
subredditWords['_all'] = []
with open(INPUT_FILE) as f:
  data = ndjson.load(f)
  #print(data[0])
  for i in data:
    sub = i['subreddit']
    if sub in SubsToProcess:
      # add to wordCounts[sub]
      if sub in subredditWords:
        subredditWords[sub] += i['body'].lower().translate(str.maketrans('', '', string.punctuation)).split()
      else:
        subredditWords[sub] = i['body'].lower().translate(str.maketrans('', '', string.punctuation)).split()

    # add to general wordcount
    subredditWords['_all'] += i['body'].lower().translate(str.maketrans('', '', string.punctuation)).split()

for sub_to_add in subreddits_add:
  SubsToProcess.append(sub_to_add)
  top_posts = reddit.subreddit(sub_to_add).top(limit=50)


  ind = 0
  STOPSTOPSTOPaaaahh = False
  subredditWords[sub_to_add] = ['the']
  for post in top_posts:
      if(STOPSTOPSTOPaaaahh == True):
          break
      for comment in post.comments:
          if(STOPSTOPSTOPaaaahh == True):
              break
          try:
            subredditWords[sub_to_add] +=comment.body.lower().translate(str.maketrans('', '', string.punctuation)).split()
            subredditWords['_all'] += comment.body.lower().translate(str.maketrans('', '', string.punctuation)).split()
          except Exception:
            print('improper comment')
            continue
          ind+=1
          if ind>added_sub_size:
              STOPSTOPSTOPaaaahh = True





print(subredditWords.keys())
subredditWordCounts = {}

print('counting words... ')
for sub in subredditWords:
  word_counts = []
  words = subredditWords[sub]

  # Counts the frequency of each word in words:
  # word_counts = [('the', 500), ('and', 450), ...]
  word_counts = list(collections.Counter(words).items())

  # for word in set(words):
  #   c = words.count(word)
  #   c = c / sub_counts[sub]
  #   word_counts.append((word, c))

  normalized = [(wc[0], wc[1] / len(subredditWords[sub]))
                for wc in word_counts]

  #print(word_counts)
  normalized.sort(key=sorting_function)
  subredditWordCounts[sub] = normalized
# word_counts = [['the', 120], ['and', 80], ]



for sub in subredditWordCounts:
  subredditWordCounts[sub] = dict(subredditWordCounts[sub])

print('normalization... ')
for word in subredditWordCounts['_all']:
  for sub in subredditWordCounts:
    if sub == '_all':
      continue
    if word in subredditWordCounts[sub]:
      subredditWordCounts[sub][word] -= subredditWordCounts['_all'][word]


subredditWordCounts['_all2'] = {}
for word in subredditWordCounts['_all']:
  subredditWordCounts['_all2'][word] = subredditWordCounts['_all'][word]
  subredditWordCounts['_all'][word] = 0

wordDimensions = set(subredditWords['_all'])
wordVectors = {}

for sub in subredditWords:
  wordVectors[sub] = []
  for word in wordDimensions:
    if word in subredditWordCounts[sub]:
      wordVectors[sub].append(subredditWordCounts[sub][word])
    else:
      wordVectors[sub].append(0)

dataCollect = []

#GRAPHING CODE STARTS--------------------------------------------------

for sub in wordVectors:
  dataCollect.append(tuple(wordVectors[sub]))



Dimensionality_data = np.array(dataCollect)

with open('Dimensionality_data', 'w') as filehandle:
    np.savetxt(filehandle, Dimensionality_data)



tsne = TSNE(n_components=2, verbose=True, perplexity=tsnePerplexity, n_iter=5000)
tsne_results = tsne.fit_transform(Dimensionality_data)

with open('subreddit-names-in-tsne-order', 'w') as filehandle:
    json.dump(list(wordVectors.keys()), filehandle)

np.savetxt('tsne-results', tsne_results)

#with open('subreddit-names-in-tsne-order', 'w') as filehandle:
    #json.dump(list(wordVectors.keys()), filehandle)

# Xtsne = tsne_results[:, 0]
# Ytsne = tsne_results[:, 1]



# pca = PCA(n_components=2)
# pca_results = pca.fit_transform(Dimensionality_data)
# Xpca = pca_results[:,0]
# Ypca = pca_results[:,1]

# fig, (ax1, ax2) = plt.subplots(1, 2)

# ax1.scatter(Xtsne, Ytsne)
# ax2.scatter(Xpca, Ypca)

# for i, label in enumerate(subredditWords):
#   ax1.annotate(label, (Xtsne[i], Ytsne[i]))
#   ax2.annotate(label, (Xpca[i], Ypca[i]))

# print("funny-science distance ", distance(subredditWordCounts['science'], subredditWordCounts['funny']))

# plt.show()

#GRAPHING CODE ENDS---------------------------------------


#maxnum = -1.1
#maxname = ''
#for subreddit in SubsToProcess:
#  if maxnum < distance(subredditWordCounts[subreddit], subredditWordCounts['gaming']):
#    maxname = subreddit
#    maxnum = distance(subredditWordCounts[subreddit], subredditWordCounts['gaming'])

#print(maxname, " has a distance of: ", maxnum, " from gaming")



#SubListMulti = {'_all': 20}

print("dimensionality: ", len(subredditWordCounts['politics']))


with open('subreddit-word-counts', 'w') as filehandle:
  json.dump(subredditWordCounts, filehandle)

with open('subs-to-process', 'w') as filehandle:
  json.dump(SubsToProcess, filehandle)


#print("funny-science distance ", common_comments2_functions.distance(subredditWordCounts['science'], subredditWordCounts['funny']))
#print("worldpolitics-libertarian distance ", common_comments2_functions.distance(subredditWordCounts['government'], subredditWordCounts['politics']))
# plot.plotBarGraphWithDict(sub_counts)

#print(subredditWordCounts)

# for i in range(0, 100):
#   print(most_common(WordList))
#   printed = most_common(WordList)
#   WordList = [i for i in WordList if i != printed]

# e.g.
# if 'Obama' occurs in _all -> 0.1
# 'Obama' occurs in politics -> 0.8
# politics - _all -> 0.7
import get_averages

get_averages.reconfigure()






with open('subreddit-word-counts', 'w') as filehandle:
  json.dump(subredditWordCounts, filehandle)

with open('subs-to-process', 'w') as filehandle:
  json.dump(SubsToProcess, filehandle)

