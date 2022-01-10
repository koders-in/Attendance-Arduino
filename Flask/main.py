from util import Client
from datetime import datetime, time
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

HASURA_URL = os.environ.get("HASURA_URL")
HASURA_HEADERS = {"X-Hasura-Admin-Secret": os.environ.get("SECRET_KEY")}

MORN_SHIFT_START = 7260
MORN_SHIFT_END = 48600
EVENING_SHIFT_START = 48660
EVENING_SHIFT_END = 7200
COOLDOWN_INTERVAL = 1800

client = Client(url=HASURA_URL, headers=HASURA_HEADERS)


def search_data(user_id):
    fetched_records = client.fetch_all_by_id(user_id)
    array_of_objects = fetched_records["data"]["attendance"]
    for object in array_of_objects:
        if object["user_id"] == user_id:
            return object


def insert_attendance(user_id: str, _time: str):
    current_time = time_to_num(_time)
    current_date = datetime.now().strftime("%Y-%m-%d")

    if current_time < MORN_SHIFT_END:  # Came morning, left morning
        if client.fetch_all_by_id(user_id)["data"]["attendance"] == []:
            client.post_time_in(user_id, _time, current_date, "dawn")
        else:
            previous_time = search_data(user_id)["dawn_clock_in"]
            if current_time - previous_time < COOLDOWN_INTERVAL:
                print("Please wait for 5 mins before trying again")
            else:
                client.post_time_out(user_id, _time, current_date, "dawn")
    elif current_time > MORN_SHIFT_END:
        # Came in the evening
        if client.fetch_all_by_id(user_id)["data"]["attendance"] == []:
            client.post_time_in(user_id, _time, current_date, "dusk")
        # Leaving in the evening
        if search_data(user_id)["dusk_clock_in"] is not None:
            previous_time = search_data(user_id)["dawn_clock_in"]
            if current_time - previous_time < COOLDOWN_INTERVAL:
                print("Please wait for 5 mins before trying again")
            else:
                client.post_time_out(user_id, _time, current_date, "dusk")
        # Came in the morning and is leaving in the evening
        if (
            search_data(user_id)["dawn_clock_in"] is not None
            and search_data(user_id)["dawn_clock_out"] is None
        ):
            client.post_time_out(user_id, _time, current_date, "dusk")


def time_to_num(time_str: str) -> int:  # Convert time to seconds
    hh, mm, ss = map(int, time_str.split(":"))
    return ss + 60 * (mm + 60 * hh)


def get_attendance(user_id: str):
    return client.fetch_all_by_id(user_id)
