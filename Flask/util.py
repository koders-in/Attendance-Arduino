from dataclasses import dataclass
from datetime import datetime
import requests


@dataclass
class Client:
    url: str
    headers: dict

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    # Helper function to make graphql queries
    def run_query(self, query: str, variables: dict = None):
        request = requests.post(
            self.url,
            headers=self.headers,
            json={"query": query, "variables": variables},
        )
        assert request.ok, f"Failed with code {request.status_code}"
        return request.json()

    # Makes mutations to post attendance values in table
    def post_time_in(self, user_id: str, _time: str, date: str, status: str):
        return self.run_query(
            """
        mutation insert_time($user_id: String!, $_time: time!, $date: date!){
         insert_attendance_one(object: {user_id: $user_id, """
            + status
            + """_clock_in: $_time, date: $date}) {
            user_id
            date
            """
            + status
            + """_clock_in
          }
        }  
        """,
            {"user_id": user_id, "_time": _time, "date": date},
        )

    # Updates the clock_out column in the table where the
    def post_time_out(self, user_id: str, _time: str, date: str, status: str):
        return self.run_query(
            """
        mutation update_clock_out($user_id: String!, $_time: time!, $date: date!){
            update_attendance(_set: {"""
            + status
            + """_clock_out: $_time}, where: {user_id: {_eq: $user_id}, _and: {date: {_eq: $date}}}) {
                affected_rows
            }
        }
        """,
            {"user_id": user_id, "_time": _time, "date": date},
        )

    # Fetch all the data for a given user_id
    def fetch_all_by_id(self, user_id: str):
        return self.run_query(
            """
        query fetch_all_records($user_id: String!) {
          attendance(where: {user_id: {_eq: $user_id}}) {
            user_id
            dusk_clock_out
            dusk_clock_in
            dawn_clock_out
            dawn_clock_in
            date
          }
        }

        """,
            {"user_id": user_id},
        )
