import os
import re
import json

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

nameset = set()
nameset.update(get_player_nameset('api_football_requester/result_220522_220529.json'))
nameset.update(get_player_nameset('api_football_requester/result_msl_220523_220529.json'))
nameset.update(get_player_nameset('api_football_requester/result_la_liga_220523_220529.json'))
nameset.update(get_player_nameset('api_football_requester/result_seria_a_220523_220529.json'))

with open('vsm/stopwords.txt', 'a',  encoding='UTF-8') as f:
    for name in nameset:
        f.write(name + '\n')