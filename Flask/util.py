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

    # def run_query(self, query: str, variables: dict, extract=False):
    def run_query(self, query: str, variables: dict = None):
        request = requests.post(
            self.url,
            headers=self.headers,
            json={"query": query, "variables": variables},
        )
        assert request.ok, f"Failed with code {request.status_code}"
        return request.json()

    # inserts clocked in time to db
    def post_time(self, _id: str, clock: str, day: str, table_name: str, status: str):
        return self.run_query(
            """
            mutation mark_attendance {
              insert_""" + table_name + """_one(object: 
                {
                  user_id: """ + _id + """, 
                  """ + status + """: " """ + clock + """ ", 
                  date: " """ + day + """ ", 
                })
              {
                id
                user_id
                clock_in
                clock_out
                date
              }
            }
        """,
        )

    # Fetch clock_in or clock_out time for a given id
    def fetch_by_id(self, _id: str, table_name: str, status: str):
        _date = datetime.now().strftime("%Y-%m-%d")
        return self.run_query(
            """
            query fetch_once {
              """ + table_name + """(where: {user_id: {_eq: """ + _id + """}, _and: {date: {_eq: " """ + _date + """ "}}}) {
                """ + status + """
              }
            }
            """,
        )

    def query_for_all(self, _id: str):
        return self.run_query(
            """
            query fetch_by_id @cached {
                    dawn(where: {user_id: {_eq: """ + _id + """ }}, order_by: {date: desc}) {
                        id
                        user_id
                        date
                        clock_in
                        clock_out
                    }
                    dusk(where: {user_id: {_eq: """ + _id + """ }}, order_by: {date: desc}) {
                    id
                    user_id
                    date
                    clock_in
                    clock_out
                    }
                }
            """
        )


