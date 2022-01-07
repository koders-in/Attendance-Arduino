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

# TODO => Fix the fetch by id method to retrieve particular columns of data
# TODO => Fix the post_time method to post time in particular columns of data

# FIXME => Convert the time to seconds for evaluation
# FIXME => For an input field update the time by verifying the date
def insert_attendance(user_id: str, _time: str):
    current_time = time_to_num(_time)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Store time data from the morning
    dawn_clock_in = client.fetch_by_id(user_id, "dawn_clock_in")
    dawn_clock_out = client.fetch_by_id(user_id, "dawn_clock_out")
    dawn_clock_out_value = dawn_clock_out["data"]["attendance"][dawn_clock_out]
    dawn_clock_in_value = dawn_clock_in["data"]["attendance"][dawn_clock_in]

    # Store time data from the evening
    dusk_clock_in = client.fetch_by_id(user_id, "dusk_clock_in")
    dusk_clock_out = client.fetch_by_id(user_id, "dusk_clock_out")
    dusk_clock_out_value = dusk_clock_out["data"]["attendance"][dusk_clock_out]
    dusk_clock_in_value = dusk_clock_in["data"]["attendance"][dusk_clock_in]

    if current_time < MORN_SHIFT_END:  # Came morning, left morning
        if dawn_clock_in_value == None:
            client.post_time(user_id, _time, current_date, "dawn_clock_in")
        elif dawn_clock_in_value is not None and dawn_clock_out_value is None:
            client.post_time(user_id, _time, current_date, "dawn_clock_out")
    else:
        if (
            dawn_clock_in_value is not None and dawn_clock_out_value is None
        ):  # Came morning, left evening
            client.post_time(user_id, _time, current_date, "dusk_clock_out")
        elif dusk_clock_in is None:
            client.post_time(
                user_id, _time, current_date, "dusk_clock_in"
            )  # Came evening left, evening
        elif dusk_clock_in is not None:
            client.post_time(user_id, _time, current_date, "dusk_clock_out")


# def insert_attendance(_id: str, _time: str):
#     current_time = time_to_num(_time)
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     if current_time < MORN_SHIFT_END:
#         status = "dawn"
#         if has_duplicates(_id, status, "clock_in"):
#             if not cooldown(_id, _time, status):
#                 # Post clock_out in the same dawn table
#                 # date_today =
#                 return client.post_time(_id, _time, current_date, status, "clock_out")
#             else:
#                 return "Wait for 5 minutes before marking your attendance again"
#         else:
#             # Post clock_in in the dawn table
#             return client.post_time(_id, _time, current_date, status, "clock_in")
#     else:
#         status = "dusk"  # Unused variable
#         print("Status set to dusk")
#         # Clock_in in dawn == YES
#         # Clock_out in dawn == NO
#         if (
#             has_duplicates(_id, "dawn", "clock_in")
#             and has_duplicates(_id, "dawn", "clock_out") == False
#         ):
#             print("Time posted in clock_out at dusk when clock_in was in dawn")
#             return client.post_time(_id, _time, current_date, "dusk", "clock_out")

#         # Clock_in in dawn == NO
#         # Clock_in in dusk == YES
#         if has_duplicates(_id, "dusk", "clock_in"):
#             print("Time posted in clock_out at dusk when clock_in was in dusk")
#             return client.post_time(_id, _time, current_date, "dusk", "clock_out")

#         # Clock_in in dawn == NO
#         # Clock_in in dusk == NO
#         if not has_duplicates(_id, "dusk", "clock_in"):
#             print('Time posted in clock_in in dusk if')
#             return client.post_time(_id, _time, current_date, "dusk", "clock_in")


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
