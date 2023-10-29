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

subreddit_to_add = 'NonCredibleDefense'
commentsnum = 200

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
        subreddit_words.append(comment.body.lower().translate(str.maketrans('', '', string.punctuation)).split())
        ind+=1
        if ind>commentsnum/2:
            STOPSTOPSTOPaaaahh = True

print(len(subreddit_words))



hot_posts = reddit.subreddit(subreddit_to_add).hot(limit=50)

ind = 0
STOPSTOPSTOPaaaahh = False
for post in hot_posts:
    if(STOPSTOPSTOPaaaahh == True):
        break
    for comment in post.comments:
        if(STOPSTOPSTOPaaaahh == True):
            break
        subreddit_words.append(comment.body.lower().translate(str.maketrans('', '', string.punctuation)).split())
        ind+=1
        if ind>commentsnum/2:
            STOPSTOPSTOPaaaahh = True

subreddit_words = [item for sublist in subreddit_words for item in sublist]
subreddit_words = subreddit_words[1:]

print(subreddit_words)
