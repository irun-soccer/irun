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

def modify_docs(corpus_path):
    nameset = get_player_nameset('api_football_requester/result_220515_220522.json')
    nameset.union(get_player_nameset('api_football_requester/result_220522_220529.json'))

    for filename in os.listdir(corpus_path):
        with open(os.path.join(corpus_path, filename), 'r', encoding='UTF-8') as f:
            tokens = f.read().split()
        modifed_tokens = []
        for token in tokens:
            token = re.sub('[“”‘]', "", token)
            if token not in nameset and not token.isdigit():
                modifed_tokens.append(token)
        with open(os.path.join(corpus_path, filename), 'w', encoding='UTF-8') as f:
            f.write(' '.join(modifed_tokens))

modify_docs('corpus2')