from redminelib import Redmine
import datetime
import requests
import json
import os


def get_profile_picture(user_id):
    url = "https://discordapp.com/api/v9/users/" + str(user_id)
    headers = {
        'Authorization': os.getenv('BOT_TOKEN'),
    }
    response = requests.request("GET", url, headers=headers)
    response = json.loads(response.text)
    try:
        return response['avatar']
    except Exception:
        return None


def get_user_data(user_id):
    redmine = Redmine('https://kore.koders.in', key=os.getenv('API_KEY'))

    user = redmine.user.get(user_id)
    for x in user:
        print(x)
    position = (user['custom_fields'][1]['value'])
    discord_id = (user['custom_fields'][0]['value'])
    issues = redmine.issue.all(limit=100, assigned_to_id=user_id)
    opened_issues, total_issues = 0, 0
    for issue in issues:
        if str(issue.status) != 'Closed':
            opened_issues += 1
        total_issues += 1

    week = []
    for i in range(0, 7):
        week.append(((datetime.datetime.now() - datetime.timedelta(days=i)).date()))

    hours = 0
    for day in week:
        time_entries = redmine.time_entry.filter(user_id=user_id, spent_on=day)
        for x in time_entries:
            hours += x.hours

    profile_picture = get_profile_picture(discord_id)
    if profile_picture:
        thumbnail_url = "https://cdn.discordapp.com/avatars/" + str(discord_id) + "/" + profile_picture + ".png"
    else:
        thumbnail_url = "https://cdn.discordapp.com/embed/avatars/0.png"
    return str(user['firstname'] + " "+ user['lastname']), position, opened_issues, total_issues, hours, thumbnail_url
