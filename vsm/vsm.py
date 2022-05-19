"""
team irun
vsm model
"""
docs_name_list = ["5~6.txt", "6~7.txt", "7~8.txt", "8~10.txt"]

for name in docs_name_list:
    f = open(r'../corpus/'+name, "rt", encoding='utf-8')
    print(f.readline())
    f.close()
