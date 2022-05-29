import re
import json
import tensorflow.keras.preprocessing.text
from twitter_crawler import get_replies

def get_player_nameset(match_json_file):
    names = set()
    with open(match_json_file, 'r') as f:
        json_data = json.load(f)
    for match in json_data:
        for player_name in json_data[match]['player']['home']:
            names.update(map(lambda x: x.lower(), player_name.split()))
        for player_name in json_data[match]['player']['away']:
            names.update(map(lambda x: x.lower(), player_name.split()))
    return names

NAME = 'Thibaut Courtois_9.0.txt'
DATE = '2022-05-28'
RATING = '9.0'

with open(f'vsm/test_query/{NAME}_{RATING}.txt', 'a',  encoding='UTF-8') as ff:
    replies = get_replies(NAME, DATE)
    for text in replies:
        text = re.sub('[“”‘]', "", text)
        text = re.sub('’', "'", text) # replace single quotation marks
        text = re.sub('(@[A-Za-z0-9]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
        tokens = tensorflow.keras.preprocessing.text.text_to_word_sequence(text) # tokenize
        for token in tokens:
            ff.write(token + ' ')
        ff.write('\n')