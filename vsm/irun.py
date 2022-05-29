import vsm

query_name = "Thibaut Courtois_9.0.txt"

f = open(r'./test_query/' + query_name, 'rt', encoding='utf-8')
query = []
while True:
    line = f.readline()
    if line == "":
        break
    elif line == "\n":
        continue
    query.append(line.strip().split(" "))
query = " ".join(sum(query, []))
print(vsm.run(query, query_name))
