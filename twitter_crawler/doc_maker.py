import re
import json
import twitter_crawler
from tensorflow.keras.preprocessing.text import text_to_word_sequence

with open('twitter_crawler/stopwords.txt', 'r') as f:
    stopwords = set(f.read().split())

def get_date(datetime):
    return datetime[:10] # YYYY-MM-DD

def pre_process(text):
    text = re.sub('’', "'", text) # replace single quotation marks
    text = re.sub('(@[A-Za-z0-9_]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
    tokens = text_to_word_sequence(text) # tokenize
    tokens = list(filter(lambda x: x not in stopwords, tokens)) # remove stopword
    return tokens

def get_interval_doc(rating):
    # [0.2 interval]
    point = 6.0
    while point < 10.0:
        if rating < point:
            return '~{:.1f}.txt'.format(point)
        point += 0.2
        
    # # [0.5 interval]
    # if rating < 6.5:
    #     return "0.0-6.5.txt"
    # elif rating < 7.0:
    #     return "6.5-7.0.txt"
    # elif rating < 7.5:
    #     return "7.0-7.5.txt"
    # elif rating < 8.0:
    #     return "7.5-8.0.txt"
    # elif rating < 8.5:
    #     return "8.0-8.5.txt"
    # else:
    #     return "8.5-9.9.txt"

def make_doc(match_json_file, corpus_path):
    with open(match_json_file, 'r') as f:
        json_data = json.load(f)

    for i, match in enumerate(json_data):

        date = get_date(json_data[match]['date'])
        print(f"\n[Match {i+1} on {date}]")

        if json_data[match]['state'] == 'Not Started':
            print("This match will start on", json_data[match]['data'])
            continue

        ratings = dict()
        ratings.update(json_data[match]['player']['home'])
        ratings.update(json_data[match]['player']['away'])

        flag = True
        for player, rating in ratings.items():
            if rating is None: # bench
                continue

            replies = twitter_crawler.get_replies(player, date)

            interval_document = get_interval_doc(float(rating))

            print(f"Now crawling {player}, reply_num: {len(replies)}, rating: {rating} -> {interval_document}")
            if len(replies) == 0:
                continue

            with open(corpus_path + interval_document, 'a', encoding='UTF-8') as f:
                for reply in replies:
                    tokens = pre_process(reply)
                    if tokens:
                        for token in tokens:
                            f.write(token + ' ')
                        f.write('\n')

make_doc('api_football_requester/result_220522_220529.json', 'corpus2/')