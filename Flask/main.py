from util import Client
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../../../Downloads/Attendance/app/.env')
load_dotenv(dotenv_path)

URL = os.environ.get("HASURA_URL")
PASSWORD = os.environ.get("SECRET_KEY")

HASURA_URL = URL
HASURA_HEADERS = {
    "X-Hasura-Admin-Secret": PASSWORD}

client = Client(url=HASURA_URL, headers=HASURA_HEADERS)

client.post_time_in(10, "12:00:00")

# def cooldown(id, time) {   FIXME => solve the double tap problem

# }
