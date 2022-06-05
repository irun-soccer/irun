import re
import json
import time
import twitter_crawler
from tensorflow.keras.preprocessing.text import text_to_word_sequence

def get_date(datetime):
    return datetime[:10] # YYYY-MM-DD

def pre_process(text):
    text = re.sub('[“”‘]', "", text)
    text = re.sub('’', "'", text) # replace single quotation marks
    text = re.sub('(@[A-Za-z0-9_]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
    tokens = text_to_word_sequence(text) # tokenize
    # tokens = list(filter(lambda x: x not in stopwords, tokens)) # remove stopword
    return tokens

def get_interval_doc(rating):
    # # [0.2 interval]
    # point = 6.0
    # while point < 10.0:
    #     if rating < point:
    #         return '~{:.1f}.txt'.format(point)
    #     point += 0.2
        
    # [0.5 interval]
    if rating < 6.5:
        return "0.0-6.5.txt"
    elif rating < 7.0:
        return "6.5-7.0.txt"
    elif rating < 7.5:
        return "7.0-7.5.txt"
    elif rating < 8.0:
        return "7.5-8.0.txt"
    else:
        return "8.0-9.9.txt"


def make_doc(match_json_file, corpus_path):
    with open(match_json_file, 'r') as f:
        json_data = json.load(f)

    skip = True

    for i, match in enumerate(json_data):
        date = get_date(json_data[match]['date'])
        print(f"\n[Match {i+1} on {date}]")

        if json_data[match]['state'] == 'Not Started':
            print("This match will start on", json_data[match]['date'])
            continue

        ratings = dict()
        ratings.update(json_data[match]['player']['home'])
        ratings.update(json_data[match]['player']['away'])

        for player, rating in ratings.items():      
            if len(player.split()) <= 1 or rating is None: # bench
                continue
            
            try:
                replies = twitter_crawler.get_replies(player, date)
            except:
                print("[...connection error occured...]")
                time.sleep(10)
                continue

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

# make_doc('api_football_requester/result_220522_220529.json', 'corpus/')
# make_doc('api_football_requester/result_la_liga_220523_220529.json', 'corpus/')
# make_doc('api_football_requester/result_seria_a_220523_220529.json', 'corpus/')
make_doc('api_football_requester/result_msl_220529_220605.json', 'corpus/')