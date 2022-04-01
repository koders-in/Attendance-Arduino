from flask import Flask, request
from flask_cors import CORS, cross_origin
from main import get_attendance, insert_attendance
import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def process_attendance():
    if request.headers.get('User-Agent') == 'ESP8266HTTPClient':
        try:
            user_id = request.get_json()['user_id']
        except KeyError as key:
            return f"unable to find {key} in request body"

        if request.method == "GET":
            try:
                offset = request.get_json()['offset']
            except KeyError:
                offset = 0
            return get_attendance(user_id, offset)

        if request.method == "POST":
            _time = datetime.datetime.now().strftime("%H:%M:%S")
            return insert_attendance(user_id, _time)
    else:
        return "Wrong request"


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True, port=3000)
    except Exception as e:
        print("Something went wrong.")
