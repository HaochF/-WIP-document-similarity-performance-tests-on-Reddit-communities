# ["_all", "reddit.com", "news", "WTF", "funny", "Music", "worldnews", "Economics", "business", "AskReddit", "programming", 
# "linux", "technology", "hardware", "nsfw", "science", "politics", "atheism", "wikipedia", "pics", "philosophy", "gaming", 
# "sex", "feminisms", "obama", "space", "lolcats", "apple", "comics", "Libertarian", "gadgets", "self", "Marijuana", 
# "environment", "offbeat", "aww", "geek", "history", "web_design", "videos", "bestof", "Boobies", "happy", "sports", 
# "Health", "ruby", "egalitarian", "energy", "MensRights", "Anarchism", "movies", "worldpolitics", "psychology", 
# "entertainment", "photography", "canada", "religion", "PS3", "humor", "guns", "ronpaul", "PalinProblem", "Design",
# "Frugal", "Chinese", "economy", "food", "Art", "conspiracy", "women", "math", "BayuAditya", "Bacon", "firefox", "scifi", 
# "gossip", "bicycling", "netsec", "independent", "AmericanPolitics", "doctorwho", "australia", "video", "Pets", "lgbt",
# "beer", "writing", "ads", "auto", "socialism", "collapse", "CommonLaw", "Israel", "government", "iphone", "ukpolitics",
# "books", "joel", "opensource", "de", "WeAreTheMusicMakers", "software", "it", "cogsci", "USPE08", "usa", "Christianity",
# "Drugs", "celebrities", "Python", "WhiteMenGoneWild", "lists", "Military", "howto", "unitedkingdom", "Pictures", "compsci",
# "Buddhism", "MMA", "MapleLinks", "Freethought", "ja", "UFOs", "redditanonoymous", "scientology", "Sexy", "travel", "Green", 
# "xkcd", "AmericanGovernment", "japan", "Metal", 
# "anime", "Ubuntu", "DIY", "islam", "haskell", "idea", "Guitar", "hackers", "civilengineering", "astro", "ArtCrit"]
import read_subreddit_data




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
    ('DIY', 'usa')
]
closest_tests = [
    'travel',
    'Art',
    'gaming',
    'business',
    'DIY',
    'UFOs',
    'Pets'
]

for pair in comparison_tests:
    word1 = pair[0]
    word2 = pair[1]
    if word1 not in read_subreddit_data.SubsToProcess or word2 not in read_subreddit_data.SubsToProcess:
        print(word1, '-', word2, ' skipped')
        continue
    cosine_dist = read_subreddit_data.cosine_dissimilarity(word1, word2)
    print(word1, '-', word2, ' cosine: ', read_subreddit_data.get_rating_cosine(cosine_dist))

for test in closest_tests:
    if test not in read_subreddit_data.SubsToProcess:
        print(test, ' skipped')
        continue
    cosine_dist, cosine_name = read_subreddit_data.get_closest_to_sub_cosine(test)
    print(test, ' closest cosine dist: ', read_subreddit_data.get_rating_cosine(cosine_dist), ', ', cosine_name)