import vsm
import result_converter

query_name = "Vinícius Júnior_7.0.txt"

f = open(r'./vsm/test_query/' + query_name, 'rt', encoding='utf-8')
query = []
while True:
    line = f.readline()
    if line == "":
        break
    elif line == "\n":
        continue
    query.append(line.strip().split(" "))
query = " ".join(sum(query, []))
result = vsm.run(query, query_name)
rating = result_converter.convert(result)

print(result)
print(rating)