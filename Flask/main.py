from util import Client
from datetime import datetime, time
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

HASURA_URL = os.environ.get("HASURA_URL")
HASURA_HEADERS = {"X-Hasura-Admin-Secret": os.environ.get("SECRET_KEY")}

# Morning shift starts from 02:00 AM
# Morning shift ends at 01:30 PM
# Evening Shift starts from 01:31 PM
# Evening Shift ends at 01:59 AM
# Cooldown interval should be of 30 minutes


client = Client(url=HASURA_URL, headers=HASURA_HEADERS)


def get_shift(_time: time):
    _time = _time.time()
    begin_time = time(2,00)
    end_time = time(13,30)
    if begin_time <= _time <= end_time:
        shift = "dawn"
    else:
        shift = "dusk"
    return shift


def is_cooldown(user_id):

def search_data(user_id):
    fetched_records = client.fetch_all_by_id(user_id)
    array_of_objects = fetched_records["data"]["attendance"]
    for object in array_of_objects:
        if object["user_id"] == user_id:
            print(object)
            return object


def insert_attendance(user_id: str, _time: str):
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(current_date)
    print(_time)

    if _time < MORN_SHIFT_END:  # TODO => Date time object should be compared
        if not client.fetch_all_by_id(user_id)["data"]["attendance"]:
            return client.post_time_in(user_id, _time, current_date, "dawn")
        else:
            previous_time = search_data(user_id)["dawn_clock_in"]
            previous_time = time_to_num(previous_time)
            # if current_time - previous_time < COOLDOWN_INTERVAL:
            #     return "Please wait for 5 mins before trying again"
            # else:
            return client.post_time_out(user_id, _time, current_date, "dawn")
    elif current_time > MORN_SHIFT_END:
        if client.fetch_all_by_id(user_id)["data"]["attendance"] == []:
            return client.post_time_in(user_id, _time, current_date, "dusk")
        if search_data(user_id)["dusk_clock_in"] is not None:
            previous_time = search_data(user_id)["dawn_clock_in"]
            previous_time = time_to_num(previous_time)
            # if current_time - previous_time < COOLDOWN_INTERVAL:
            #     return "Please wait for 5 mins before trying again"
            # else:
            return client.post_time_out(user_id, _time, current_date, "dusk")
        if (
            search_data(user_id)["dawn_clock_in"] is not None
            and search_data(user_id)["dawn_clock_out"] is None
        ):
            return client.post_time_out(user_id, _time, current_date, "dusk")


def time_to_num(time_str: str) -> int:  
    hh, mm, ss = map(int, time_str.split(":"))
    return ss + 60 * (mm + 60 * hh)


def get_attendance(user_id: str):
    return client.fetch_all_by_id(user_id)
