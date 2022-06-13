from twitter_crawler import query_maker
from vsm import vsm, result_converter

player_name = "Ajdin Hrustic"
match_date = "2022-06-08"

query = query_maker.make_query_string(player_name, match_date)
result = vsm.run(query, player_name)
rating = result_converter.convert(result)

print(result)
print(rating)