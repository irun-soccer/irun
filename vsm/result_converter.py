max_value_weight = 5

def convert(result):
    if type(result) == dict:
        result = list(result.values())

    result[result.index(max(result))] *= max_value_weight

    normalized_result = list(map(lambda x: x/sum(result), result))
    docs_weight = [5, 6.5, 7.5, 8.5, 10]

    rating = sum([i*j for i, j in zip(normalized_result, docs_weight)])

    return rating