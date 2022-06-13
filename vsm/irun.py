import result_converter, vsm

query_file = r"vsm\test_query\Mohamed Salah_7.2.txt"

with open(query_file, 'rt', encoding='utf-8') as f:
    query = f.read()
result = vsm.run(query, "")
rating = result_converter.convert(result)

print(result)
print(rating)
