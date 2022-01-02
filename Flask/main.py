from util import Client
from datetime import datetime, time
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'env')
load_dotenv(dotenv_path)

HASURA_URL = os.environ.get("HASURA_URL")
HASURA_HEADERS = {"X-Hasura-Admin-Secret": os.environ.get("SECRET_KEY")}

MORN_SHIFT_START = 7260
MORN_SHIFT_END = 48600
EVENING_SHIFT_START = 48660
EVENING_SHIFT_END = 7200
COOLDOWN_INTERVAL = 1800

client = Client(url=HASURA_URL, headers=HASURA_HEADERS)


def insert_attendance(_id: str, _time: str):
    current_time = time_to_num(_time)
    current_date = datetime.now().strftime("%Y-%m-%d")
    if current_time < MORN_SHIFT_END:
        status = 'dawn'
        if has_duplicates(_id, status, 'clock_in'):
            if not cooldown(_id, _time, status):
                # Post clock_out in the same dawn table
                # date_today =
                return client.post_time(_id, _time, current_date, status, 'clock_out')
            else:
                return "Wait for 5 minutes before marking your attendance again"
        else:
            # Post clock_in in the dawn table
            return client.post_time(_id, _time, current_date, status, 'clock_in')
    else:
        status = 'dusk'  # Unused variable
        # Clock_in in dawn == YES
        # Clock_out in dawn == NO
        if has_duplicates(_id, 'dawn', 'clock_in') and has_duplicates(_id, 'dawn', 'clock_out') == False:
            return client.post_time(_id, _time, current_date, 'dusk', 'clock_out')

        # Clock_in in dawn == NO
        # Clock_in in dusk == YES
        if has_duplicates(_id, 'dusk', 'clock_in'):
            return client.post_time(_id, _time, current_date, 'dusk', 'clock_out')

        # Clock_in in dawn == NO
        # Clock_in in dusk == NO
        if not has_duplicates(_id, 'dusk', 'clock_in'):
            return client.post_time(_id, _time, current_date, 'dusk', 'clock_in')


def time_to_num(time_str: str) -> int:  # Convert time to seconds
    hh, mm, ss = map(int, time_str.split(':'))
    return ss + 60 * (mm + 60 * hh)


def has_duplicates(_id: str, table_name: str, status: str) -> bool:
    data = client.fetch_by_id(_id, table_name, status)
    try:
        extracted_time = data['data'][table_name][0][status]
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
        status = 'dawn'
    else:
        status = 'dusk'
    fetched_time = client.fetch_by_id(_id, table_name, status)
    formatted_time = fetched_time['data'][table_name + '_by_pk']['clock_in']
    previous_time = time_to_num(formatted_time)
    current_time = time_to_num(cooldown_timer)
    if current_time - previous_time < COOLDOWN_INTERVAL:
        return True
    else:
        return False


def get_attendance(_id: str):
    return client.query_for_all(_id)