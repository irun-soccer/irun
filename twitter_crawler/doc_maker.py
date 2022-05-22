import re
import json
import twitter_crawler
from tensorflow.keras.preprocessing.text import text_to_word_sequence
#from nltk.corpus import stopwords

with open('twitter_crawler/stopwords.txt', 'r') as f:
    stopwords = set(f.read().split())

def get_date(datetime):
    return datetime[:10] # YYYY-MM-DD

def pre_process(text):
    text = re.sub('@.+', '', text) # remove mention
    tokens = text_to_word_sequence(text) # tokenize (+ remove stopword)
    return tokens

def make_doc(match_json_file, corpus_path):
    with open(match_json_file, 'r') as f:
        json_data = json.load(f)

    for match in json_data:
        date = get_date(json_data[match]['date'])

        ratings = dict()
        ratings.update(json_data[match]['player']['home'])
        ratings.update(json_data[match]['player']['away'])

        for player, rating in ratings.items():
            try:
                replies = twitter_crawler.get_replies(player, date)

                rating = float(rating)
                if rating < 6.0:
                    interval_document = "0.0-6.0.txt"
                elif rating < 7.0:
                    interval_document = "6.0-7.0.txt"
                elif rating < 7.5:
                    interval_document = "7.0-7.5.txt"
                elif rating < 8.0:
                    interval_document = "7.5-8.0.txt"
                elif rating < 8.5:
                    interval_document = "8.0-8.5.txt"
                else:
                    interval_document = "8.5-9.9.txt"

                print(f"Now crawling {player} on {date}, rating: {rating} -> {interval_document}")

                with open(corpus_path + interval_document, 'a', encoding='UTF-8') as f:
                    for reply in replies:
                        tokens = pre_process(reply)
                        f.write(tokens + '\n')
            except:
                pass

#make_doc('api_football_requester/result.json', 'corpus/')