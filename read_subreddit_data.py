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
import praw
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta


def sorting_function(t):
  return t[1]


with open('PASSWORD.txt', 'r') as f:
    pw = f.read()

reddit = praw.Reddit(
    client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
    client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
    username = 'tester78780',
    password = pw,
    user_agent = "<ReplyCommentBot1.0>"
)

model = SentenceTransformer('bert-base-nli-mean-tokens')

#with open('subreddit_descs') as jsons:
#    subreddit_descs = json.load(jsons)

subreddit_descs = {}

with open('subreddit-word-counts') as json_file1:
    global subredditWordCounts 
    subredditWordCounts = json.load(json_file1)

with open('subs-to-process') as file1:
    global SubsToProcess
    SubsToProcess = json.load(file1)

with open('values_cosine') as json_file:
    distances_cosine = [0]
    for line in json_file:
        distances_cosine.append(float(line))

with open('values_euclid') as file:
    distances_euclid = [0]
    for line in file:
        distances_euclid.append(float(line))

with open('values_BERT') as file:
    distances_BERT = [0]
    for line in file:
        distances_BERT.append(float(line))

def update():
    with open('subreddit-word-counts') as json_file1:
        globals()["subredditWordCounts"] = json.load(json_file1)

    with open('subs-to-process') as file1:
        globals()["SubsToProcess"] = json.load(file1)

    with open('values_cosine') as json_file:
        globals()["distances_cosine"] = [0]
        for line in json_file:
            globals()["distances_cosine"].append(float(line))

    with open('values_euclid') as file:
        globals()["distances_euclid"] = [0]
        for line in file:
            globals()["distances_euclid"].append(float(line))

    with open('values_BERT') as file:
        globals()["distances_BERT"] = [0]
        for line in file:
            globals()["distances_BERT"].append(float(line))



def get_user_dict(totalSubreddits, normalize):
    user_dict = {}
    for sub in totalSubreddits:
        if sub in SubsToProcess:
            if sub not in user_dict.keys():
                user_dict[sub] = 1

            else :
                user_dict[sub] += 1
    if normalize:
        for sub in user_dict.keys():
            if user_dict[sub] > 10:
                members = reddit.subreddit(sub).subscribers
                if members == 0:
                    user_dict[sub] = 0
                else:
                    user_dict[sub] = user_dict[sub] + 240*user_dict[sub]/math.sqrt(members)
            else:
                user_dict[sub] = 0
    return {k: v for k, v in sorted(user_dict.items(), key=lambda item: -item[1])}

def get_user_dict_unrestricted(totalSubreddits, normalize):
    user_dict = {}
    for sub in totalSubreddits:
        if sub not in user_dict.keys():
            user_dict[sub] = 1

        else :
            user_dict[sub] += 1

    if normalize:
        for sub in user_dict.keys():
            if user_dict[sub] > 10:
                members = reddit.subreddit(sub).subscribers
                if members <10000:
                    user_dict[sub] = 0
                else:
                    user_dict[sub] = user_dict[sub] + 240*user_dict[sub]/math.sqrt(members)
            else:
                user_dict[sub] = 0
    return {k: v for k, v in sorted(user_dict.items(), key=lambda item: -item[1])}




def get_user_dists(sub, normalize):
    hot_posts = reddit.subreddit(sub).hot(limit=75)
    
    time_ago = datetime.utcnow() - timedelta(hours=2400)


    top_posts = reddit.subreddit(sub).top(limit=1000)

    top_posts = [
        x for x in top_posts
        if datetime.utcfromtimestamp(x.created_utc) >= time_ago
    ]

    if len(top_posts) > 45:
        top_posts = top_posts[:44]    


    totalSubreddits = []
    for post in hot_posts:
        try:
            auth_name = post.author.name
            comments = reddit.redditor(auth_name).comments.new(limit=25)
            for comment in comments:
                sub_name = comment.subreddit.display_name
                if sub_name != sub:
                    totalSubreddits.append(sub_name)
        except Exception:
            continue

    for post in top_posts:
        try:
            auth_name = post.author.name
            comments = reddit.redditor(auth_name).comments.new(limit=25)
            for comment in comments:
                sub_name = comment.subreddit.display_name
                if sub_name != sub:
                    totalSubreddits.append(sub_name)
        except Exception:
            continue
        
    return(get_user_dict(totalSubreddits, normalize), get_user_dict_unrestricted(totalSubreddits, normalize))

def get_farthest_from_user(user_dict):
    return common_comments2_functions.get_farthest_from_weights(user_dict, subredditWordCounts, SubsToProcess)

def distance(sub_A, sub_B):
    return common_comments2_functions.distance(subredditWordCounts[sub_A], subredditWordCounts[sub_B])

def cosine_dissimilarity(sub_A, sub_B):
    return common_comments2_functions.cosine_dis(subredditWordCounts[sub_A], subredditWordCounts[sub_B])

def BERT_dissimilarity(sub_A, sub_B):
    try:
        #with open('subreddit_descs') as jsons:
            #subreddit_descs = json.load(jsons)
            
        if sub_A not in subreddit_descs.keys():
            subreddit_descs[sub_A] = sub_A + ': ' + reddit.subreddit(sub_A).public_description
            #with open('subreddit_descs', 'w') as filehandle:
                #json.dump(subreddit_descs, filehandle)

        if sub_B not in subreddit_descs.keys():
            subreddit_descs[sub_B] = sub_B + ': ' + reddit.subreddit(sub_B).public_description
            #with open('subreddit_descs', 'w') as filehandle:
                #json.dump(subreddit_descs, filehandle)
    except Exception:
        return -1

    descs = [subreddit_descs[sub_A], subreddit_descs[sub_B]]

    if len(descs[0]) <=1 or len(descs[1]) <= 1:
        return -1

    descembed = model.encode(descs)

    score = cosine_similarity(
        [ descembed[1]],
        [ descembed[0]]
    )

    return (1-score[0][0])

def BERT_dissimilarity_desc(desc_A, desc_B):
    descs = [desc_A, desc_B]

    if len(descs[0]) <=1 or len(descs[1]) <= 1:
        return -1

    descembed = model.encode(descs)

    score = cosine_similarity(
        [ descembed[1]],
        [ descembed[0]]
    )

    return (1-score[0][0])



def get_rating_euclid(result):
    length = len(distances_euclid)
    splits = 100

    for i in range(1, splits+1):
        if result <= distances_euclid[int(i*length/splits)-1]:
            return round(1-i*1/splits, 2)
        
        
def get_rating_cosine(result):
    length = len(distances_cosine)
    splits = 100

    for i in range(1, splits+1):
        if result <= distances_cosine[int(i*length/splits)-1]:
            return round(1-i*1/splits, 2)


def get_rating_BERT(result):
    length = len(distances_BERT)
    splits=100

    for i in range(1, splits+1):
        if result <= distances_BERT[int(i*length/splits)-1]:
            return round(1-i*1/splits, 2)


def get_closest_to_sub_euclid(sub):
    min = 10000
    save = "AAAAAAAAAHHHHHHHHHHHH"
    for name in SubsToProcess:
        if name == sub or name == 'reddit.com':
            continue
        dist = common_comments2_functions.distance(subredditWordCounts[sub], subredditWordCounts[name])
        if dist < min:
            min = dist
            save = name
    return min, save

def get_close_recs_euclid(sub, num):
    pairs = []
    for name in SubsToProcess:
        if name == sub or name == 'reddit.com':
            continue
        dist = common_comments2_functions.distance(subredditWordCounts[sub], subredditWordCounts[name])
        pairs.append([name, dist])

    pairs.sort(key=sorting_function)

    names = []
    dists = []
    for i in range(0, num):
        names.append(pairs[i][0])
        dists.append(pairs[i][1])
    return names, dists

def get_closest_to_sub_cosine(sub):
    min = 10000
    save = "AAAAAAAAAHHHHHHHHHHHH"
    for name in SubsToProcess:
        if name == sub or name == 'reddit.com':
            continue
        dist = common_comments2_functions.cosine_dis(subredditWordCounts[sub], subredditWordCounts[name])
        #dist = math.sqrt(dist**2)
        if dist < min:
            min = dist
            save = name
    return min, save


def get_close_recs_cos(sub, num):
    pairs = []
    for name in SubsToProcess:
        if name == sub or name == 'reddit.com':
            continue
        dist = common_comments2_functions.cosine_dis(subredditWordCounts[sub], subredditWordCounts[name])
        pairs.append([name, dist])

    pairs.sort(key=sorting_function)

    names = []
    dists = []
    for i in range(0, num):
        names.append(pairs[i][0])
        dists.append(pairs[i][1])
    return names, dists


def get_closest_to_sub_BERT(sub):
    min = 10000
    save = "AAAAAAAAAHHHHHHHHHHHH"
    for name in SubsToProcess:
        if name == sub or name == 'reddit.com':
            continue
        dist = BERT_dissimilarity(sub, name)
        if dist < min and dist != -1:
            min = dist
            save = name
    return min, save


def get_closest_to_sub_BERT_fast(sub, speed):
    min = 10000
    save = "AAAAAAAAAHHHHHHHHHHHH"
    ind = 0
    for name in SubsToProcess:
        ind += 1
        if ind%speed != 0:
            continue
        if name == sub or name == 'reddit.com':
            continue
        dist = BERT_dissimilarity(sub, name)
        if dist < min and dist != -1:
            min = dist
            save = name
    return min, save


def get_close_recs_BERT_fast(sub, num, speed):
    pairs = []
    ind = 0
    for name in SubsToProcess:
        ind+= 1
        if ind%speed != 0:
            continue
        if name == sub or name == 'reddit.com':
            continue
        dist = BERT_dissimilarity(sub, name)
        if dist != -1:
            pairs.append([name, dist])

    pairs.sort(key=sorting_function)

    names = []
    dists = []

    for i in range(0, num):
        if i >= len(pairs):
            names.append("extraneous")
            dists.append(100)
        else:
            names.append(pairs[i][0])
            dists.append(pairs[i][1])
    return names, dists
#print(common_comments2_functions.get_farthest_from_weights({'offbeat': 20, 'gaming': 20}, subredditWordCounts, SubsToProcess))




