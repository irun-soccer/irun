import math
"""
team irun
vsm model
"""
docs_name_list = ["0.0-6.5", "6.5-7.0", "7.0-7.5", "7.5-8.0", "8.0-8.5", "8.5-9.9"]

# 특정 문서 d 에서의 특정 단어 t 의 등장 횟수. docs_tf[d][t] = num
docs_tf = {}
# 특정 단어 t 가 등장한 문서의 수. docs_df[t] = num
# docs_df = {}
# docs_tf_idf = {}


def make_tf_idf_docs():
    docs_num = 0
    # 각 문서의 전처리는 전부 되어 있다고 가정함.
    for name in docs_name_list:
        docs_num += 1
        f = open(r'../corpus/'+name+'.txt', "rt", encoding='utf-8')
        docs_tf[name] = {}

        docs_len = 0
        while True:
            line = f.readline()
            if line == "":
                break
            elif line == "\n":
                continue

            for word in line.strip().split(" "):
                if word == "":
                    continue
                docs_len += 1
                word = word.lower()
                # get tf value
                if word in docs_tf:
                    docs_tf[name][word] += 1
                else:
                    docs_tf[name][word] = 1

        # normalize
        for word, tf in docs_tf[name].items():
            docs_tf[name][word] = tf / docs_len
        f.close()

    return docs_tf


print(make_tf_idf_docs())
