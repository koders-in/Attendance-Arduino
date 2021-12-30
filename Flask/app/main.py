from util import Client
from datetime import datetime, time
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

URL = os.environ.get("HASURA_URL")
PASSWORD = os.environ.get("SECRET_KEY")

HASURA_URL = URL
HASURA_HEADERS = {
    "X-Hasura-Admin-Secret": PASSWORD}

MORN_SHIFT_START = 7260
MORN_SHIFT_END = 48600
EVENING_SHIFT_START = 48660
EVENING_SHIFT_END = 7200
COOLDOWN_INTERVAL = 1800

client = Client(url=HASURA_URL, headers=HASURA_HEADERS)

# TODO => If clock_in has no value in dawn or dusk, insert as clock_in in the right table. If clock_in exists, register as clock out.


def insert_attendance(id, time):
    now = datetime.now()
    current_time = time_to_num(now.strftime("%H:%M:%S"))
    requires_cooldown = cooldown(id, time)
    if current_time < MORN_SHIFT_END and requires_cooldown == False:
        client.post_time_in_dawn(id, time)


def time_to_num(time_str: str) -> int:          # Convert time to seconds
    hh, mm, ss = map(int, time_str.split(':'))
    return ss + 60*(mm + 60*hh)


def cooldown(id: int, time_in: str) -> bool:
    fetched_time = client.fetch_by_id_from_dawn(id)
    formatted_time = fetched_time['data']['dawn_by_pk']['clock_in']
    previous_time = time_to_num(formatted_time)
    current_time = time_to_num(time_in)
    if current_time - previous_time > COOLDOWN_INTERVAL:
        return True
    else:
        return False


print(time_to_num("11:30:00") - time_to_num("11:00:00"))
