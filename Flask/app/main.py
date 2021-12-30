from util import Client
from datetime import datetime
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


client = Client(url=HASURA_URL, headers=HASURA_HEADERS)

# client.post_time_in(21, "20:00:00")


# TODO => If clock_in has no value in dawn or dusk, insert as clock_in in the right table. If clock_in exists, register as clock out.
def insert_attendance(id, time):
    # time_in = self.fetch_time_in(id)
    # formatted_time = time_in['data']['dawn_by_pk']['clock_in']
    now = datetime.now()
    current_time = time_to_num(now.strftime("%H:%M:%S"))
    if current_time < MORN_SHIFT_END:
        client.post_time_in(id, time)


def time_to_num(time_str: str) -> int:          # Convert time to seconds
    hh, mm, ss = map(int, time_str.split(':'))
    return ss + 60*(mm + 60*hh)


insert_attendance(1, 3)


def cooldown(id: int, time: str):  # TODO => solve the double tap problem
    fetched_time = client.fetch_by_id_from_dawn(id)
    formatted_time = fetched_time['data']['dawn_by_pk']['clock_in']
    time_in_seconds = time_to_num(formatted_time)


# def no_out_without_in() {     TODO => If time in exists and another entry is made after 30 mins, that will be registered as clock_out

# }
