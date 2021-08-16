from django.http import HttpResponse
import requests
import json as json_lib

# View to format and return language stats from GitHub API

repo_names_url = 'https://api.github.com/users/WillSztej/repos'

def index(request):
    repo_info = requests.get(repo_names_url)
    json = repo_info.json()
    print(json)
    repo_names = []
    for repo in json:
        repo_names.append(repo['full_name'])
    print(repo_names)

    lang_stats = {}
    byte_sum = 0

    for repo in repo_names:
        url = f'https://api.github.com/repos/{repo}/languages'
        lang_stat_request = requests.get(url)
        json = lang_stat_request.json()
        for language in json:
            if language not in lang_stats:
                lang_stats[language] = json[language]
                byte_sum += json[language]
                continue
            curr_bytes = lang_stats[language]
            add_bytes = json[language]
            lang_stats[language] = curr_bytes + add_bytes
            byte_sum += add_bytes

    languages = lang_stats.keys()
    lang_percentage = {}
    formatted_list = []
    for language in languages:
        lang_percentage[language] = lang_stats[language] / byte_sum * 100
        formatted_list.append({'category': language, 'value': round(lang_percentage[language], 4)})

    print(formatted_list)
    return HttpResponse(json_lib.dumps(formatted_list))
