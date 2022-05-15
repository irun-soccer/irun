import api_football_secret as secret
import requests
import json
from collections import defaultdict


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
    fixture_query_string = {"league" : "39", "season": "2021"}
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
    print(fixture_dict)


if __name__ == "__main__":
    main()
