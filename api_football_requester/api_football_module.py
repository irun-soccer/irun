import api_football_secret as secret
import requests
import json
from collections import defaultdict
from datetime import date, datetime, timedelta


def get_response_as_json(url, headers, query):
    if query == "":
        response = requests.request("GET", url, headers=headers)
    else:
        response = requests.request("GET", url, headers=headers, params=query)
    parsed = json.loads(response.text)
    return parsed


def main():
    team_crawl_url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    team_query_string = {"league" : "39", "season": "2021"}
    # Fixed query target league as England Premier League id = 39, target season = 2021

    headers = {
        "X-RapidAPI-Host": secret.x_rapidapi_host,
        "X-RapidAPI-Key": secret.x_rapidapi_key
    }
    
    team_info_json = get_response_as_json(team_crawl_url, headers, team_query_string)
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    team_name_dict = defaultdict(str)
    for i in range(len(team_info_json['response'])):
        # print(parsed['response'][i]['team'])
        team_name = team_info_json['response'][i]['team']['name']
        team_code = int(team_info_json['response'][i]['team']['id'])
        team_name_dict[team_code] = team_name

    fixture_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    fixture_query_string = {"league" : "39", "season": "2021", "from": datetime.strftime((datetime.now() - timedelta(7)), "%Y-%m-%d"), "to": date.today().strftime("%Y-%m-%d")}
    # print(json.dumps(get_response_as_json(fixture_url, headers, fixture_query_string), indent=2))
    fixture_info_json = get_response_as_json(fixture_url, headers, fixture_query_string)
    fixture_dict = defaultdict(dict)
    for i in range(len(fixture_info_json['response'])):
        fixture_info = fixture_info_json['response'][i]['fixture']
        fixture_team_info = fixture_info_json['response'][i]['teams']
        fixture_score = fixture_info_json['response'][i]['score']
        # print('[INFO] : ', end='')
        # print(fixture_info)
        # print('[TEAM] : ', end='')
        # print(fixture_team_info)
        # print('[SCORE] : ', end='')
        # print(fixture_score)
        fixture_dict[fixture_info['id']] = dict()
        fixture_dict[fixture_info['id']]['date'] = fixture_info['date']
        fixture_dict[fixture_info['id']]['state'] = fixture_info['status']['long']
        fixture_dict[fixture_info['id']]['team'] = dict()
        fixture_dict[fixture_info['id']]['team']['home'] = fixture_team_info['home']['id']
        fixture_dict[fixture_info['id']]['team']['away'] = fixture_team_info['away']['id']
        fixture_dict[fixture_info['id']]['score'] = fixture_score['fulltime']

    lineup_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups"
    print("Getting fixture data from " + datetime.strftime((datetime.now() - timedelta(7)), "%Y-%m-%d") + " to " + date.today().strftime("%Y-%m-%d"))
    print("Crawling On Process Total " + str(len(fixture_dict)) + " fixture player information..")
    for key, values in fixture_dict.items():
        lineup_url_with_fixture = lineup_url + "?fixture=" + str(key)
        print("Crawling fixture info by id = " + str(key) + " ...")
        lineup_info_json = get_response_as_json(lineup_url_with_fixture, headers, "")
        fixture_dict[key]['player'] = dict()
        home_team_id = fixture_dict[key]['team']['home']
        away_team_id = fixture_dict[key]['team']['away']
        fixture_dict[key]['player']['home'] = list()
        fixture_dict[key]['player']['away'] = list()
        try:
            for k in range(2):
                if lineup_info_json['response'][k]['team']['id'] == home_team_id:
                    for i in range(len(lineup_info_json['response'][k]['startXI'])):
                        fixture_dict[key]['player']['home'].append(lineup_info_json['response'][k]['startXI'][i]['player']['name'])
                    for i in range(len(lineup_info_json['response'][k]['substitutes'])):
                        fixture_dict[key]['player']['home'].append(lineup_info_json['response'][k]['substitutes'][i]['player']['name'])
                elif lineup_info_json['response'][k]['team']['id'] == away_team_id:
                    for i in range(len(lineup_info_json['response'][k]['startXI'])):
                        fixture_dict[key]['player']['away'].append(lineup_info_json['response'][k]['startXI'][i]['player']['name'])
                    for i in range(len(lineup_info_json['response'][k]['substitutes'])):
                        fixture_dict[key]['player']['away'].append(lineup_info_json['response'][k]['substitutes'][i]['player']['name'])
        except KeyError:
            print("KeyError at fixture number + " + str(key) + ". Please wait and retry.")
        except IndexError:
            print("Index out of range " + str(key) + ". May be fixture not started yet?")
        # print(fixture_dict[key])

    result_file_name = "api_football_requester/result.json"
    result = json.dumps(fixture_dict)
    result_file = open(result_file_name, "w")
    result_file.write(result)
    result_file.close()

    print("\nJob Finished.")
    

if __name__ == "__main__":
    main()
