import read_subreddit_data
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import praw

def sorting_function(t):
  return t[1]


def reconfigure():
    
    distances_euclid = [['d', 1]]
    for i in range(0, len(read_subreddit_data.SubsToProcess)):
        for j in range(i+1, len(read_subreddit_data.SubsToProcess)):
            word1 = read_subreddit_data.SubsToProcess[i]
            word2 = read_subreddit_data.SubsToProcess[j]
            distances_euclid.append(['' + word1 + '-' + word2, read_subreddit_data.distance(word1, word2)])

    distances_euclid = distances_euclid[1:]
    distances_euclid.sort(key=sorting_function)



    distances_cos = [['d', 1]]
    for i in range(0, len(read_subreddit_data.SubsToProcess)):
        for j in range(i+1, len(read_subreddit_data.SubsToProcess)):
            word1 = read_subreddit_data.SubsToProcess[i]
            word2 = read_subreddit_data.SubsToProcess[j]
            distances_cos.append(['' + word1 + '-' + word2, read_subreddit_data.cosine_dissimilarity(word1, word2)])

    distances_cos = distances_cos[1:]
    distances_cos.sort(key=sorting_function)



    euclid_connections = ['d']
    for pair in distances_euclid:
        euclid_connections.append(pair[0])
    euclid_connections = euclid_connections[1:]

    with open('connections_euclid', 'w') as filehandle:
        json.dump(euclid_connections, filehandle)


    cosine_connections = ['d']
    for pair in distances_cos:
        cosine_connections.append(pair[0])
    cosine_connections = cosine_connections[1:]

    with open('connections_cosine', 'w') as filehandle:
        json.dump(cosine_connections, filehandle)
 

    euclid_dist = distances_euclid.copy()
    for i in range(0, len(euclid_dist)):
        distances_euclid[i] = euclid_dist[i][1]
    mid = len(distances_euclid) // 2
    res = (distances_euclid[mid] + distances_euclid[~mid]) / 2
    print('average distances euclid: ', res)


    with open('values_euclid', 'w') as filehandle:
        np.savetxt(filehandle, distances_euclid)


    cos_dist = distances_cos.copy()
    for i in range(0, len(cos_dist)):
        distances_cos[i] = cos_dist[i][1]
    mid = len(distances_cos) // 2
    res = (distances_cos[mid] + distances_cos[~mid]) / 2
    print('averages distance cos: ', res)


    with open('values_cosine', 'w') as filehandle:
        np.savetxt(filehandle, distances_cos)




    with open('PASSWORD.txt', 'r') as f:
        pw = f.read()

    reddit = praw.Reddit(
        client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
        client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
        username = 'tester78780',
        password = pw,
        user_agent = "<ReplyCommentBot1.0>"
    )

    subreddit_descs = {}
    '''
    subreddit_descs = ['placeholder']
    for sub in read_subreddit_data.SubsToProcess:
        pdesc = reddit.subreddit(sub).public_description
        if len(pdesc) > 1:
            subreddit_descs.append(pdesc)
    model = SentenceTransformer('bert-base-nli-mean-tokens')


    descembed = model.encode(subreddit_descs[1:])

    arr = cosine_similarity(
        descembed,
        descembed
    )

    arr_flat = [element for sublist in arr for element in sublist]

    arr_flat.sort()


    with open('values_BERT', 'w') as filehandle:
        np.savetxt(filehandle, arr_flat)
    '''





    subreddit_descs = {}
    sum_not_in = 0

    distances_BERT = [['d', 1]]
    for i in range(0, len(read_subreddit_data.SubsToProcess)):
        for j in range(i+1, len(read_subreddit_data.SubsToProcess)):
            word1 = read_subreddit_data.SubsToProcess[i]
            word2 = read_subreddit_data.SubsToProcess[j]

            dist = read_subreddit_data.BERT_dissimilarity(word1, word2)
            if dist == -1:
                continue
            distances_BERT.append(['' + word1 + '-' + word2, dist])

    print('sum not in: ', sum_not_in)

    distances_BERT = distances_BERT[1:]
    distances_BERT.sort(key=sorting_function)

    BERT_connections = ['d']
    for pair in distances_BERT:
        BERT_connections.append(pair[0])
    BERT_connections = BERT_connections[1:]

    with open('connections_BERT', 'w') as filehandle:
        json.dump(BERT_connections, filehandle)
    

    BERT_dist = distances_BERT.copy()
    for i in range(0, len(BERT_dist)):
        distances_BERT[i] = BERT_dist[i][1]
    mid = len(distances_BERT) // 2
    res = (distances_BERT[mid] + distances_BERT[~mid]) / 2
    print('averages distance BERT: ', res)


    with open('values_BERT', 'w') as filehandle:
        np.savetxt(filehandle, distances_BERT)
    return 0


