import json

from pandas import interval_range
import twitter_crawler

def get_date(datetime):
    return datetime[:10] # YYYY-MM-DD


# test
with open('api_football_requester/result.json', 'r') as f:
    json_data = json.load(f)

for match in json_data:
    date = get_date(json_data[match]['date'])

    ratings = dict()
    ratings.update(json_data[match]['player']['home'])
    ratings.update(json_data[match]['player']['away'])

    for player, rating in ratings.items():
        try:
            replies = twitter_crawler.get_replies(player, date)

            # temporary interval
            rating = float(rating)
            if rating < 4.0:
                interval_document = "0~4.txt"
            elif rating < 5.0:
                interval_document = "4~5.txt"
            elif rating < 6.0:
                interval_document = "5~6.txt"
            elif rating < 7.0:
                interval_document = "6~7.txt"
            elif rating < 8.0:
                interval_document = "7~8.txt"
            else:
                interval_document = "8~10.txt"

            print(f"Now crawling {player} on {date}, rating: {rating} -> {interval_document}")
            with open('corpus/'+interval_document, 'a', encoding='UTF-8') as f:
                for reply in replies:
                    f.write(reply)
        except:
            pass