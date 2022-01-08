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

    # Store time data from the evening
    dusk_clock_in_value = search_data(user_id)["dusk_clock_in"]

    if current_time < MORN_SHIFT_END:  # Came morning, left morning
        if client.fetch_all_by_id(user_id)["data"]["attendance"] == []:
            client.post_time_in(
                user_id, _time, current_date, current_date, "dawn_clock_in"
            )
        else:
            client.post_time_out(user_id, _time, current_date, "dawn_clock_out")
    elif current_time > MORN_SHIFT_END:
        # Retrieve time data from the morning
        dawn_clock_out_value = search_data(user_id)["dawn_clock_out"]
        dawn_clock_in_value = search_data(user_id)["dawn_clock_in"]
        if (
            dawn_clock_in_value is not None and dawn_clock_out_value is None
        ):  # Came morning, left evening
            client.post_time_out(user_id, _time, current_date, "dusk_clock_out")
        elif dusk_clock_in_value is None:
            client.post_time_in(
                user_id, _time, current_date, "dusk_clock_in"
            )  # Came evening left, evening
        elif dusk_clock_in_value is not None:
            client.post_time_out(user_id, _time, current_date, "dusk_clock_out")


def time_to_num(time_str: str) -> int:  # Convert time to seconds
    hh, mm, ss = map(int, time_str.split(":"))
    return ss + 60 * (mm + 60 * hh)


def has_duplicates(_id: str, table_name: str, status: str) -> bool:
    data = client.fetch_by_id(_id, table_name, status)
    try:
        extracted_time = data["data"][table_name][0][status]
    except IndexError:
        return False
    except TypeError:
        return False
    if extracted_time is None:
        return False
    else:
        return True


def cooldown(_id: str, cooldown_timer: str, table_name: str) -> bool:
    current_time = time_to_num(datetime.now().strftime("%H:%M:%S"))
    if current_time < MORN_SHIFT_END:
        status = "dawn"
    else:
        status = "dusk"
    fetched_time = client.fetch_by_id(_id, table_name, status)
    formatted_time = fetched_time["data"][table_name + "_by_pk"]["clock_in"]
    previous_time = time_to_num(formatted_time)
    current_time = time_to_num(cooldown_timer)
    if current_time - previous_time < COOLDOWN_INTERVAL:
        return True
    else:
        return False


def get_attendance(_id: str):
    return client.query_for_all(_id)


insert_attendance("5", "11:00:00")
insert_attendance("5", "17:00:00")

# temp = search_data("2")["dawn_clock_out"]
# print(temp)
