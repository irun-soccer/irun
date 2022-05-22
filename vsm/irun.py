import vsm

# docs_tf_idf = vsm.make_tf_idf_docs()
input_query_vector = {}

# f = open(r'test_input.txt', 'rt', encoding='utf-8')
docs = vsm.make_tf_idf_docs()
docs = vsm.run("d")
print(docs)