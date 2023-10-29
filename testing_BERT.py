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

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



with open('PASSWORD.txt', 'r') as f:
    pw = f.read()

reddit = praw.Reddit(
    client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
    client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
    username = 'tester78780',
    password = pw,
    user_agent = "<ReplyCommentBot1.0>"
)






desc1 = reddit.subreddit('business').public_description
desc2 = reddit.subreddit('Economics').public_description
model = SentenceTransformer('bert-base-nli-mean-tokens')

descs = [desc1, desc2]
descembed = model.encode(descs)

print(desc1)
print(desc2)

print(cosine_similarity(
    [descembed[0]],
    [descembed[1]]
))