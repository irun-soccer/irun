"""
team irun
vsm model
"""
docs_name_list = ["5~6.txt", "6~7.txt", "7~8.txt", "8~10.txt"]
docs_num = 0
# 특정 문서 d 에서의 특정 단어 t 의 등장 횟수. docs_tf[d][t] = num
docs_tf = {}
# 특정 단어 t 가 등장한 문서의 수. docs_df[t] = num
docs_df = {}


# 각 문서의 전처리는 전부 되어 있다고 가정함.
for name in docs_name_list:
    docs_num += 1
    f = open(r'../corpus/'+name, "rt", encoding='utf-8')
    docs_tf[name] = {}

    while True:
        line = f.readline()
        if line == "":
            break
        elif line == "\n":
            continue

        for word in line.strip().split(" "):
            word = word.lower()
            # get tf value
            if word in docs_tf:
                docs_tf[name][word] += 1
            else:
                docs_tf[name][word] = 1
                # get df value
                if word in docs_df:
                    docs_df[word] += 1
                else:
                    docs_df[word] = 1
    f.close()

print(docs_tf)