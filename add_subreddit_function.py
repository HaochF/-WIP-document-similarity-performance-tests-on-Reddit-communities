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
import get_averages
import read_subreddit_data
import numpy as np

import os
import requests
from praw.models import MoreComments
from prawcore import NotFound
from prawcore.exceptions import Forbidden


def sorting_function(t):
    return -t[1]

def add_sub(name, numcomments):
    subreddit_to_add = name
    commentsnum = numcomments

    with open('PASSWORD.txt', 'r') as f:
        pw = f.read()

    reddit = praw.Reddit(
        client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
        client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
        username = 'tester78780',
        password = pw,
        user_agent = "<ReplyCommentBot1.0>"
    )

    with open('subreddit-word-counts') as json_file1:
        subredditWordCounts = json.load(json_file1)

    with open('subs-to-process') as file1:
        SubsToProcess = json.load(file1)

    SubsToProcess.append(subreddit_to_add)

    top_posts = reddit.subreddit(subreddit_to_add).top(limit=50)

    ind = 0
    STOPSTOPSTOPaaaahh = False
    subreddit_words = [['the']]
    for post in top_posts:
        if(STOPSTOPSTOPaaaahh == True):
            break
        for comment in post.comments:
            if(STOPSTOPSTOPaaaahh == True):
                break
            try:
                subreddit_words.append(comment.body.lower().translate(str.maketrans('', '', string.punctuation)).split())
            except Exception:
                continue
            ind+=1
            if ind>commentsnum/2:
                STOPSTOPSTOPaaaahh = True




    hot_posts = reddit.subreddit(subreddit_to_add).hot(limit=50)

    ind = 0
    STOPSTOPSTOPaaaahh = False
    for post in hot_posts:
        if(STOPSTOPSTOPaaaahh == True):
            break
        for comment in post.comments:
            if(STOPSTOPSTOPaaaahh == True):
                break
            try:
                subreddit_words.append(comment.body.lower().translate(str.maketrans('', '', string.punctuation)).split())
            except Exception:
                continue
            ind+=1
            if ind>commentsnum/2:
                STOPSTOPSTOPaaaahh = True

    subreddit_words = [item for sublist in subreddit_words for item in sublist]
    subreddit_words = subreddit_words[1:]


    word_counts = []
    words = subreddit_words

    # Counts the frequency of each word in words:
    # word_counts = [('the', 500), ('and', 450), ...]
    word_counts = list(collections.Counter(words).items())

    # for word in set(words):
    #   c = words.count(word)
    #   c = c / sub_counts[sub]
    #   word_counts.append((word, c))

    normalized = [(wc[0], wc[1] / len(subreddit_words))
                for wc in word_counts]

    #print(word_counts)

    

    normalized.sort(key=sorting_function)
    subredditWordCounts[subreddit_to_add] = normalized
    subredditWordCounts[subreddit_to_add] = dict(subredditWordCounts[subreddit_to_add])


    for word in subredditWordCounts['_all2']:
        if word in subredditWordCounts[subreddit_to_add]:
            subredditWordCounts[subreddit_to_add][word] -= subredditWordCounts['_all2'][word]






    with open('values_cosine') as json_file:
        distances_cos = [0]
        for line in json_file:
            distances_cos.append(float(line))

    distances_cos = distances_cos[1:]

    with open('values_euclid') as file:
        distances_euclid = [0]
        for line in file:
            distances_euclid.append(float(line))

    distances_euclid = distances_euclid[1:]




    with open('subreddit-word-counts', 'w') as filehandle:
        json.dump(subredditWordCounts, filehandle)

    with open('subs-to-process', 'w') as filehandle:
        json.dump(SubsToProcess, filehandle)

    read_subreddit_data.update()
    for j in range(0, len(read_subreddit_data.SubsToProcess)):
        if read_subreddit_data.SubsToProcess[j] == subreddit_to_add:
            continue
        word1 = subreddit_to_add
        word2 = read_subreddit_data.SubsToProcess[j]
        distances_euclid.append(read_subreddit_data.distance(word1, word2))

    distances_euclid.sort()
    mid = len(distances_euclid) // 2
    res = (distances_euclid[mid] + distances_euclid[~mid]) / 2


    with open('values_euclid', 'w') as filehandle:
        np.savetxt(filehandle, distances_euclid)


    read_subreddit_data.update()
    for j in range(0, len(read_subreddit_data.SubsToProcess)):
        if read_subreddit_data.SubsToProcess[j] == subreddit_to_add:
            continue
        word1 = subreddit_to_add
        word2 = read_subreddit_data.SubsToProcess[j]
        distances_cos.append(read_subreddit_data.cosine_dissimilarity(word1, word2))

    distances_cos.sort()
    mid = len(distances_cos) // 2
    res = (distances_cos[mid] + distances_cos[~mid]) / 2



    with open('values_cosine', 'w') as filehandle:
        np.savetxt(filehandle, distances_cos)


