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
import read_subreddit_data

import os
import requests
from praw.models import MoreComments
from prawcore import NotFound
from prawcore.exceptions import Forbidden

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sub = 'investing'

with open('PASSWORD.txt', 'r') as f:
    pw = f.read()

reddit = praw.Reddit(
    client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
    client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
    username = 'tester78780',
    password = pw,
    user_agent = "<ReplyCommentBot1.0>"
)

top_posts = reddit.subreddit(sub).hot(limit=50)

totalSubreddits = []
for post in top_posts:
    auth_name = post.author.name
    comments = reddit.redditor(auth_name).comments.new(limit=50)
    for comment in comments:
        sub_name = comment.subreddit.display_name
        if sub_name != sub:
            totalSubreddits.append(sub_name)

print(read_subreddit_data.get_user_dict_unrestricted(totalSubreddits))