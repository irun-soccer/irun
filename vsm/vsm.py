import numpy as np
import matplotlib.pyplot as plt

"""
team irun
vsm model
"""
docs_name_list = ["0.0-6.5", "6.5-7.0", "7.0-7.5", "7.5-8.0", "8.0-9.9"]
# docs_name_list = ["~6.0", "~6.2", "~6.4", "~6.6", "~6.8", "~7.0", "~7.2", "~7.4",
#                  "~7.6", "~7.8", "~8.0", "~8.2", "~8.4", "~8.6", "~8.8", "~9.0",
#                  "~9.4"]
# 특정 문서 d 에서의 특정 단어 t 의 등장 횟수. docs_tf[d][t] = num
docs_tf = {}
# 특정 단어 t 가 등장한 문서의 수. docs_df[t] = num
docs_df = {}
# docs_tf_idf = {}
LIMIT = 3265

stopword = []


def make_tf_idf_docs():
    docs_num = 0
    if not stopword:
        f = open(r'stopwords.txt', "rt", encoding='utf-8')
        s_word = f.readline()
        while True:
            if s_word == "":
                break
            stopword.append(s_word.strip())
            s_word = f.readline()
        f.close()

    for name in docs_name_list:
        docs_num += 1
        f = open(r'../corpus/'+name+'.txt', "rt", encoding='utf-8')
        docs_tf[name] = {}
        corpus = []
        docs_len = 0
        while True:
            line = f.readline()
            corpus.append(line)
            if line == "":
                break
            elif line == "\n":
                continue

            for word in line.strip().split(" "):
                if word == "" or word in stopword:
                    continue
                docs_len += 1
                word = word.lower()
                # get tf value
                if word in docs_tf[name]:
                    docs_tf[name][word] += 1
                else:
                    docs_tf[name][word] = 1
                    if word not in docs_df:
                        docs_df[word] = 0

        if len(docs_tf[name]) > LIMIT:
            docs_len = 0
            sorted_dict = sorted(docs_tf[name].items(), key=lambda x: x[1], reverse=True)
            docs_tf[name] = {}
            for key, value in sorted_dict[:LIMIT]:
                docs_tf[name][key] = value
                docs_len += value

        f.close()

    return docs_tf


def run(query, query_name=""):
    if len(docs_tf) == 0:
        print("please make if-idf docs first.")
        return
    query_vector = {}
    docs_vector = {}
    cos_sim = {}
    # init vector
    for word, value in docs_df.items():
        query_vector[word] = 0
        docs_vector[word] = 0
    for word in query.strip().split(" "):
        if word in query_vector:
            query_vector[word] = 1
    # dict to list
    query_vector = list(query_vector.values())

    for name in docs_name_list:
        # init docs vec
        for word, value in docs_vector.items():
            docs_vector[word] = 0
        # update docs vec
        for word in docs_tf[name]:
            docs_vector[word] = docs_tf[name][word]
        # dict to list
        docs_vector_list = list(docs_vector.values())
        if np.linalg.norm(query_vector) * np.linalg.norm(docs_vector_list) != 0:
            cos_sim[name] = np.dot(query_vector, docs_vector_list) / (np.linalg.norm(query_vector) * np.linalg.norm(docs_vector_list))
        else:
            cos_sim[name] = 0

    x, y = [], []
    # print cos sim
    for key, value in cos_sim.items():
        print(key, ": ", value, len(docs_tf[key]))
        tmp = key.split("-")
        if tmp[0] == "0.0":
            tmp[0] = "5.0"
        x.append((float(tmp[0]) + float(tmp[1])) / 2)
        y.append(value)

    # plot
    plt.figure(figsize=(8, 8))
    plt.title("cosine similarity, query: " + query_name)

    plt.plot(x, y)
    plt.tight_layout()
    plt.show()

    return "relevant docs: " + max(cos_sim, key=cos_sim.get)


make_tf_idf_docs()
# print("relevant docs:", run("nice"))
