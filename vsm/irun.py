import vsm

f = open(r'test_input.txt', 'rt', encoding='utf-8')
query = []
while True:
    line = f.readline()
    if line == "":
        break
    elif line == "\n":
        continue
    query.append(line.strip().split(" "))
query = " ".join(sum(query, []))
print(vsm.run(query))
