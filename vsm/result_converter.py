from math import exp

exp_multiple = 50

def convert(result):
    if type(result) == dict:
        result = list(result.values())

    normalized_result = list(map(lambda x: exp(x/sum(result)*exp_multiple), result))
    normalized_result = list(map(lambda x: x/sum(normalized_result), normalized_result))

    docs_weight = [5, 6.5, 7.5, 8.5, 10]

    rating = sum([i*j for i, j in zip(normalized_result, docs_weight)])

    return rating
