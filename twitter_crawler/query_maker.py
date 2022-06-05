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

def make_query_file(name, date):
    with open(f'vsm/test_query/{name}.txt', 'a',  encoding='UTF-8') as ff:
        replies = get_replies(name, date)
        for text in replies:
            text = re.sub('[“”‘]', "", text)
            text = re.sub('’', "'", text) # replace single quotation marks
            text = re.sub('(@[A-Za-z0-9]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
            tokens = tensorflow.keras.preprocessing.text.text_to_word_sequence(text) # tokenize
            for token in tokens:
                ff.write(token + ' ')
            ff.write('\n')

def make_query_string(name, date):
    query_string = ""
    replies = get_replies(name, date)
    for text in replies:
        text = re.sub('[“”‘]', "", text)
        text = re.sub('’', "'", text) # replace single quotation marks
        text = re.sub('(@[A-Za-z0-9]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
        tokens = tensorflow.keras.preprocessing.text.text_to_word_sequence(text) # tokenize
        for token in tokens:
            query_string += token + ' '
        query_string += '\n'