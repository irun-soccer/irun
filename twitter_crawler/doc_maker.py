import re
import json
import twitter_crawler
from tensorflow.keras.preprocessing.text import text_to_word_sequence

def get_date(datetime):
    return datetime[:10] # YYYY-MM-DD

def pre_process(text):
    text = re.sub('@.+', '', text) # remove mention
    tokens = text_to_word_sequence(text) # tokenize (+ remove stopword)
    return tokens

def make_doc(match_json_file, corpus_path):
    with open(match_json_file, 'r') as f:
        json_data = json.load(f)

    for i, match in enumerate(json_data):
        date = get_date(json_data[match]['date'])
        print(f"\n[Match {i+1} on {date}]")

        ratings = dict()
        ratings.update(json_data[match]['player']['home'])
        ratings.update(json_data[match]['player']['away'])

        for player, rating in ratings.items():
            if rating is None: # bench
                continue

            replies = twitter_crawler.get_replies(player, date)

            rating = float(rating)
            if rating < 6.5:
                interval_document = "0.0-6.5.txt"
            elif rating < 7.0:
                interval_document = "6.5-7.0.txt"
            elif rating < 7.5:
                interval_document = "7.0-7.5.txt"
            elif rating < 8.0:
                interval_document = "7.5-8.0.txt"
            elif rating < 8.5:
                interval_document = "8.0-8.5.txt"
            else:
                interval_document = "8.5-9.9.txt"

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

make_doc('api_football_requester/result_220515_220522.json', 'corpus/')