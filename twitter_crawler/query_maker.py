import re
import tensorflow.keras.preprocessing.text
from twitter_crawler import get_replies

with open('vsm/test_input2.txt', 'a',  encoding='UTF-8') as ff:
    replies = get_replies('Gerson', '2022-05-21')

    for text in replies:
        text = re.sub('’', "'", text) # replace single quotation marks
        text = re.sub('(@[A-Za-z0-9]+)|(\w+:\/\/\S+)', '', text) # remove mention, link
        tokens = tensorflow.keras.preprocessing.text.text_to_word_sequence(text) # tokenize
        with open('twitter_crawler/stopwords.txt', 'r') as f:
            stopwords = set(f.read().split())
        tokens = list(filter(lambda x: x not in stopwords, tokens)) # remove stopword
        for token in tokens:
            ff.write(token + ' ')
        ff.write('\n')