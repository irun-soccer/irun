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

nameset = get_player_nameset('api_football_requester/result_220515_220522.json')
nameset.union(get_player_nameset('api_football_requester/result_220522_220529.json'))

NAME = 'alaba'
DATE = '2022-05-29'
RATING = '7.5'

nameset.update(NAME.split())

with open(f'vsm/test_query/{NAME}_{RATING}.txt', 'a',  encoding='UTF-8') as ff:
    replies = get_replies(NAME, DATE)
    for text in replies:
        text = re.sub('[“”‘]', "", text)
        text = re.sub('’', "'", text) # replace single quotation marks
        text = re.sub('(@[A-Za-z0-9]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
        tokens = tensorflow.keras.preprocessing.text.text_to_word_sequence(text) # tokenize
        with open('twitter_crawler/stopwords.txt', 'r') as f:
            stopwords = set(f.read().split())
        tokens = list(filter(lambda x: x not in stopwords, tokens)) # remove stopword
        tokens = list(filter(lambda x: x not in nameset, tokens)) # remove name
        tokens = list(filter(lambda x: not x.isdigit(), tokens)) # remove single number
        for token in tokens:
            ff.write(token + ' ')
        ff.write('\n')