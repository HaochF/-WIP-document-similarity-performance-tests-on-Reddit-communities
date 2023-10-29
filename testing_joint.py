
import read_subreddit_data
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import praw
from prawcore import NotFound
import add_subreddit_function

with open('PASSWORD.txt', 'r') as f:
    pw = f.read()

reddit = praw.Reddit(
    client_id = 'bGx7g2Oogzhs3hq2pb2tBg',
    client_secret = 'ZnIWmqJPZVCnCoWAxN6Ze-G0mx_IJw',
    username = 'tester78780',
    password = pw,
    user_agent = "<ReplyCommentBot1.0>"
)

def find_word(word):
    for sub in read_subreddit_data.SubsToProcess:
        if word.lower() == sub.lower():
            return sub
    print('mispelled/doesnt exist: ', word)
    exit()

def sub_exists(sub):
    exists = True
    try:
        top_posts = reddit.subreddit(sub).hot(limit=50)
        if len(list(top_posts))<10: exists = False
    except Exception:
        exists = False
    return exists

numberposts = 30
dopairs = False
doClose = False
doRecs = True
doBest = False

fastBERT = True

comparison_tests = [
    ('news', 'gaming'),
    ('worldnews', 'news'),
    ('DIY', 'books'),
    ('Economics', 'business'),
    ('AmericanPolitics', 'business'),
    ('hackers', 'Python'),
    ('scientology', 'australia'),
    ('science', 'technology'),
    ('MMA', 'writing'),
    ('socialism', 'economy'),
    ('Economics', 'economy'),
    ('cogsci', 'Python'),
    ('Military', 'guns'),
    ('Drugs', 'Marijuana'),
    ('funny', 'humor'),
    ('Libertarian', 'environment'),
    ('space', 'photography'),
    ('space', 'technology'),
    ('Libertarian', 'Freethought'),
    ('religion', 'Buddhism'),
    ('movies', 'entertainment'),
    ('PS3', 'gaming'),
    ('AmericanPolitics', 'obama'),
    ('howto', 'DIY'),
    ('howto', 'obama'),
    ('socialism', 'Anarchism'),
    ('psychology', 'philosophy'),
    ('DIY', 'usa'),
    ('Chinese', 'usa'),
    ('Overwatch', 'usa'),
    ('Overwatch', 'Military'),
    ('Overwatch', 'AmericanGovernment'),
    ('Overwatch', 'gaming'),
    ('linux', 'gaming'),
    ('NonCredibleDefense', 'worldnews'),
    ('NonCredibleDefense', 'DIY')
]
closest_tests = [
#    'osugame'
    'gaming'
    ,'travel'
    ,'Art'
    ,'DIY'
    ,'Pets'
    ,'WeAreTheMusicMakers'
    ,'worldpolitics'
    ,'Buddhism'
    ,'Overwatch'
]



if dopairs:
    print('pairs')
    print('----------++++++++++-----------')
    for pair in comparison_tests:
        print('-------------------------------')
        word1 = pair[0]
        word2 = pair[1]
        try:
            if reddit.subreddit(word1).subreddit_type != 'public':
                print(word1, 'not public')
                continue
        except Exception:
            print(word1, 'private/banned')
            continue
        try:
            if reddit.subreddit(word2).subreddit_type != 'public':
                print(word2, 'not public')
                continue
        except Exception:
            print(word2, 'private/banned')
            continue

        if sub_exists(word1) == False:
            print(word1, 'too small/inactive')
            continue
        
        if sub_exists(word2) == False:
            print(word2, 'too small/inactive')
            continue

        #if word1 not in read_subreddit_data.SubsToProcess or word2 not in read_subreddit_data.SubsToProcess:
        #    print(word1, '-', word2, ' skipped')
        #    continue
        if word1 not in read_subreddit_data.SubsToProcess:
            print('adding ', word1)
            add_subreddit_function.add_sub(word1, 400)
        if word2 not in read_subreddit_data.SubsToProcess:
            print('adding ', word2)
            add_subreddit_function.add_sub(word2, 400)
        euclid_dist = read_subreddit_data.distance(word1, word2)
        cosine_dist = read_subreddit_data.cosine_dissimilarity(word1, word2)
        BERT_dist = read_subreddit_data.BERT_dissimilarity(word1, word2)

        print(word1, '-', word2, ' euclid: ', read_subreddit_data.get_rating_euclid(euclid_dist))
        print(word1, '-', word2, ' cosine: ', read_subreddit_data.get_rating_cosine(cosine_dist))
        if BERT_dist == -1:
            print(word1, '-', word2,' BERT SKIPPED')
        else:
            print(word1, '-', word2, ' BERT: ', read_subreddit_data.get_rating_BERT(BERT_dist))

    print('-------------------------------')
    print('-------------------------------')
    print('-------------------------------')



with open('connections_BERT') as file:
        connections_BERT = json.load(file)

with open('values_BERT') as file:
        distances_BERT_read = [0]
        for line in file:
            distances_BERT_read.append(float(line))
        distances_BERT_read = distances_BERT_read[1:]


if doClose:
    print('closest')
    print('----------++++++++++-----------')
    for test in closest_tests:
        try:
            if reddit.subreddit(test).subreddit_type != 'public':
                print(test, 'skipped/not public')
                continue
        except Exception:
            print(test, 'skipped/private')

        if test not in read_subreddit_data.SubsToProcess:
            print(test, ' skipped/not in list')
            continue
        if sub_exists(test) == False:
            print(test, ' skipped/small')
            continue
        if test not in read_subreddit_data.SubsToProcess:
            print(test, ' skipped')
            continue
        if sub_exists(test) == False:
            print(test, ' skipped')
            continue

        euclid_dist, euclid_name = read_subreddit_data.get_closest_to_sub_euclid(test)
        print(test, ' closest euclid dist: ', read_subreddit_data.get_rating_euclid(euclid_dist), ', ', euclid_name)

        cosine_dist, cosine_name = read_subreddit_data.get_closest_to_sub_cosine(test)
        print(test, ' closest cosine dist: ', read_subreddit_data.get_rating_cosine(cosine_dist), ', ', cosine_name)

        if fastBERT == True:
            bert_dist, bert_name = read_subreddit_data.get_closest_to_sub_BERT_fast(test, 20)
            print(test, ' close BERT dist: ', read_subreddit_data.get_rating_BERT(bert_dist), ', ', bert_name)
        
        else:
            for i in range(0, len(connections_BERT)):
                connection = connections_BERT[i]
                dist = distances_BERT_read[i]
                words = connection.split('-')
                if test == words[0]:
                    print(test, ' closest BERT dist: ', read_subreddit_data.get_rating_BERT(dist), ', ', words[1])
                    break
                if test == words[1]:
                    print(test, ' closest BERT dist: ', read_subreddit_data.get_rating_BERT(dist), ', ', words[0])
                    break
    

        print('top 5 user-based recs for ', test, ':')
        dict_, dict_unres = read_subreddit_data.get_user_dists(test)
        ind = 0
        for x in dict_.keys():
            print(x, 'at closeness', dict_[x])
            ind += 1
            if ind > 4:
                break

        print('top 5 user-based recs unrestricted for ', test, ':')
        ind = 0
        for x in dict_unres.keys():
            print(x, 'at closeness', dict_unres[x])
            ind += 1
            if ind > 4:
                break


if doRecs:
    print('Recommendations')
    for test in closest_tests:
        print('----------++++++++++-----------')
        print('----------', test ,'-----------')
        print('----------++++++++++-----------')
        try:
            if reddit.subreddit(test).subreddit_type != 'public':
                print(test, 'skipped/not public')
                continue
        except Exception:
            print(test, 'skipped/private')
            continue

        if test not in read_subreddit_data.SubsToProcess:
            print('adding ', test)
            add_subreddit_function.add_sub(test, 500)
        if sub_exists(test) == False:
            print(test, ' skipped/small')
            continue
        


        names, dists = read_subreddit_data.get_close_recs_euclid(test, 5)
        print('euclid recommendations for ', test, ':')
        out = ""
        for name in names:
            out += name + " "
        print(out)
        out = ""
        for dist in dists:
            out += str(read_subreddit_data.get_rating_euclid(dist)) + " "
        print(out)

        ind = 0
        outcos = ""
        outBERT = ""
        for x in names:
            if x not in read_subreddit_data.SubsToProcess:
                print('adding ', x)
                add_subreddit_function.add_sub(x, 500)
            outcos += str(read_subreddit_data.get_rating_cosine(read_subreddit_data.cosine_dissimilarity(x, test))) + " "
            outBERT += str(read_subreddit_data.get_rating_BERT(read_subreddit_data.BERT_dissimilarity(x, test))) + " "
            ind += 1
            if ind > 4:
                break

        print("cosine opinion: ")
        print(outcos)
        print("BERT opinion: ")
        print(outBERT)
        print('-------------------------------')


        names, dists = read_subreddit_data.get_close_recs_cos(test, 5)
        print('cosine recommendations for ', test, ':')
        out = ""
        for name in names:
            out += name + " "
        print(out)
        out = ""
        for dist in dists:
            out += str(read_subreddit_data.get_rating_cosine(dist)) + " "
        print(out)

        ind = 0
        outeuc = ""
        outBERT = ""
        for x in names:
            if x not in read_subreddit_data.SubsToProcess:
                print('adding ', x)
                add_subreddit_function.add_sub(x, 500)
            outeuc += str(read_subreddit_data.get_rating_euclid(read_subreddit_data.distance(x, test))) + " "
            outBERT += str(read_subreddit_data.get_rating_BERT(read_subreddit_data.BERT_dissimilarity(x, test))) + " "
            ind += 1
            if ind > 4:
                break
        print("euclid opinion: ")
        print(outeuc)
        print("BERT opinion: ")
        print(outBERT)
        print('-------------------------------')


        if fastBERT == True:
            names, dists = read_subreddit_data.get_close_recs_BERT_fast(test, 5, 20)
            print('rough BERT recommendations for ', test, ':')
            out = ""
            for name in names:
                out += name + " "
            print(out)
            out = ""
            for dist in dists:
                out += str(read_subreddit_data.get_rating_BERT(dist)) + " "
            print(out)

            ind = 0
            outcos = ""
            outeuc = ""
            for x in names:
                if x not in read_subreddit_data.SubsToProcess:
                    print('adding ', x)
                    add_subreddit_function.add_sub(x, 500)
                outcos += str(read_subreddit_data.get_rating_cosine(read_subreddit_data.cosine_dissimilarity(x, test))) + " "
                outeuc += str(read_subreddit_data.get_rating_euclid(read_subreddit_data.distance(x, test))) + " "
                ind += 1
                if ind > 4:
                    break
            print("euclid opinion: ")
            print(outeuc)
            print("cosine opinion: ")
            print(outcos)
            print('-------------------------------')
        
        else:
            for i in range(0, len(connections_BERT)):
                connection = connections_BERT[i]
                dist = distances_BERT_read[i]
                words = connection.split('-')
                if test == words[0]:
                    print(test, ' closest BERT dist: ', read_subreddit_data.get_rating_BERT(dist), ', ', words[1])
                    break
                if test == words[1]:
                    print(test, ' closest BERT dist: ', read_subreddit_data.get_rating_BERT(dist), ', ', words[0])
                    break

            print('-------------------------------')
    

        print('top 5 user-based recs for ', test, ':')
        dict_, dict_unres = read_subreddit_data.get_user_dists(test, True)
        ind = 0
        out1 = ""
        out2 = ""
        outcos = ""
        outeuc = ""
        outBERT = ""
        for x in dict_unres.keys():
            if x not in read_subreddit_data.SubsToProcess:
                print('adding ', x)
                add_subreddit_function.add_sub(x, 500)
            outcos += str(read_subreddit_data.get_rating_cosine(read_subreddit_data.cosine_dissimilarity(x, test))) + " "
            outeuc += str(read_subreddit_data.get_rating_euclid(read_subreddit_data.distance(x, test))) + " "
            outBERT += str(read_subreddit_data.get_rating_BERT(read_subreddit_data.BERT_dissimilarity(x, test))) + " "
            out1 += x + " "
            out2 += str(dict_unres[x]) + " "
            ind += 1
            if ind > 4:
                break
        print(out1)
        print("euclid opinion: ")
        print(outeuc)
        print("cosine opinion: ")
        print(outcos)
        print("BERT opinion: ")
        print(outBERT)
       # print(out2)
        print('-------------------------------')


        print('top 5 user-based recs unormalized for ', test, ':')
        dict_, dict_unres = read_subreddit_data.get_user_dists(test, False)
        ind = 0
        out0 = ""
        out1 = ""
        out2 = ""
        outpercent = ""
        outcos = ""
        outeuc = ""
        outBERT = ""
        total = 0
        for x in dict_unres.keys():
            total = total + dict_unres[x]
        temp_dict = {}
        for x in dict_unres.keys():
            if x not in read_subreddit_data.SubsToProcess:
                print('adding ', x)
                add_subreddit_function.add_sub(x, 500)
            outcos += str(read_subreddit_data.get_rating_cosine(read_subreddit_data.cosine_dissimilarity(x, test))) + " "
            outeuc += str(read_subreddit_data.get_rating_euclid(read_subreddit_data.distance(x, test))) + " "
            outBERT += str(read_subreddit_data.get_rating_BERT(read_subreddit_data.BERT_dissimilarity(x, test))) + " "
            placeholder, newdict = read_subreddit_data.get_user_dists(x, False)
            if test in newdict.keys():
                out1 += x + "(mutual):" + str(newdict[test]) + ' '
                temp_dict[x] = dict_unres[x] * (newdict[test]+1)**1.5
            else: 
                out1 += x + "(no mutual) "
                temp_dict[x] = dict_unres[x]
            out2 += str(dict_unres[x]) + " "
            outpercent += str(dict_unres[x]/total)[:6] + "% "
            
            ind += 1
            if ind > 9:
                break
        temp_dict = {k: v for k, v in sorted(temp_dict.items(), key=lambda item: -item[1])}
        for x in temp_dict.keys():
            out0 = out0 + x + " "
        print(out0)
        print("raw: ")
        print(out1)
        print("percentage from sample: ")
        print(outpercent)
        print("euclid opinion: ")
        print(outeuc)
        print("cosine opinion: ")
        print(outcos)
        print("BERT opinion: ")
        print(outBERT)
       # print(out2)

        print('-------------------------------')
        print('-------------------------------')
        print('-------------------------------')

        





if doBest:
    print('close dists')
    print('----------++++++++++-----------')
    with open('connections_euclid') as json_file:
        connections_euclid = json.load(json_file)

    with open('connections_cosine') as file:
        connections_cosine = json.load(file)

    with open('connections_BERT') as file:
        connections_BERT = json.load(file)


    with open('values_cosine') as json_file:
        distances_cosine_read = [0]
        for line in json_file:
            distances_cosine_read.append(float(line))
        distances_cosine_read = distances_cosine_read[1:]

    with open('values_euclid') as file:
        distances_euclid_read = [0]
        for line in file:
            distances_euclid_read.append(float(line))
        distances_euclid_read = distances_euclid_read[1:]

    with open('values_BERT') as file:
        distances_BERT_read = [0]
        for line in file:
            distances_BERT_read.append(float(line))
        distances_BERT_read = distances_BERT_read[1:]






    for i in range(1, numberposts):
        print(connections_euclid[i], ' is at euclid distance ', read_subreddit_data.get_rating_euclid(distances_euclid_read[i]))

    for i in range(1, numberposts):
        print(connections_cosine[i], ' is at cosine distance ', read_subreddit_data.get_rating_cosine(distances_cosine_read[i]))

    for i in range(1, numberposts):
        print(connections_BERT[i], ' is at BERT distance ', read_subreddit_data.get_rating_BERT(distances_BERT_read[i]))
