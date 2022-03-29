from redminelib import Redmine
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from main import get_attendance, insert_attendance
import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)


@app.route('/<_id>', methods=['POST', 'GET'])
@cross_origin()
def process_attendance(_id):
    if _id is None:
        return "CAN'T FIND ID"

    if request.method == "GET":
        return get_attendance(_id)

    if request.method == "POST":
        _time = datetime.datetime.now().strftime("%H:%M:%S")
        return insert_attendance(_id, _time)


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def send_user_data():
    if request.method == 'GET':
        return "Server is running... Hello world!"
    if request.method == 'POST':
        if not request.get_json():
            return "Something went wrong."
        username = request.get_json()["username"]
        password = request.get_json()["password"]

        redmine = Redmine('https://kore.koders.in', username=username, password=password)

        user = {
            "name": str(redmine.user.get('me')),
            "user_id": redmine.user.get('me').id
        }

        # PROJECTS
        projects = redmine.project.all(limit=100)
        projects_opened = 0
        for project in projects:
            if project.status:
                projects_opened += 1
        project = {
            "opened": projects_opened,
            "total": projects.total_count
        }

        # ISSUES
        user_id = redmine.user.get('me').id
        issues = redmine.issue.all(limit=100, assigned_to_id=user_id)
        opened_issues, total_issues = 0, 0
        for issue in issues:
            if str(issue.status) != 'Closed':
                opened_issues += 1
            total_issues += 1

        issues_dict = {
            "opened": opened_issues,
            "total": total_issues
        }

        # SPENT TIME LAST 7 DAYS
        spent_time = {}
        week = []
        for i in range(0, 7):
            week.append(((datetime.datetime.now() - datetime.timedelta(days=i)).date()))

        for day in week:
            time_entries = redmine.time_entry.filter(user_id=user_id, spent_on=day)
            hours = 0
            for x in time_entries:
                hours += x.hours
            spent_time[day.strftime("%d/%m/%Y")] = hours

        data = {
            "user": user,
            "project": project,
            "issue": issues_dict,
            "spent_time": spent_time
        }

        json_data = json.dumps(data, indent=4)
        return json_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)
