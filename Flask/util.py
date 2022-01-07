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
    def post_time(self, user_id: str, _time: str, date: str, column_name: str):
        self.run_query(
            """
          mutation ($user_id: String!, $_time: time!, date: date!)
            insert_attendance(objects: {user_id: $user_id, date: $date, """
            + column_name
            + """_clock_in: $_time}){
              user_id
              """
            + column_name
            + """_clock_in
              date
            }
          }
        """
        )

    # Fetch all the data for a given user_id
    def fetch_all_by_id(self, user_id: str):
        return self.run_query(
            """
        query MyQuery($user_id: String!) {
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

    # def post_time(self, _id: str, clock: str, day: str, table_name: str, status: str):
    #     print("Inside post_time")
    #     print(
    #         self.run_query(
    #             """
    #       mutation mark_attendance {
    #         insert_"""
    #             + table_name
    #             + """_one(object:
    #           {
    #             user_id: """
    #             + _id
    #             + """,
    #             """
    #             + status
    #             + """: " """
    #             + clock
    #             + """ ",
    #             date: " """
    #             + day
    #             + """ ",
    #           })
    #         {
    #           id
    #           user_id
    #           clock_in
    #           clock_out
    #           date
    #         }
    #       }
    #   """,
    #         )
    #     )
    #     print("query suc")

    # Fetch clock_in or clock_out time for dawn or dusk
    # def fetch_time(self, user_id:str, status: str, date: str):

    # Fetch clock_in or clock_out time for a given id
    # def fetch_by_id(self, user_id: str, status: str):
    #     _date = datetime.now().strftime("%Y-%m-%d")
    #     return self.run_query(
    #         """
    #         query fetch_once {
    #           """
    #         + table_name
    #         + """(where: {user_id: {_eq: """
    #         + _id
    #         + """}, _and: {date: {_eq: " """
    #         + _date
    #         + """ "}}}) {
    #             """
    #         + status
    #         + """
    #           }
    #         }
    #         """,
    #     )

    # def query_for_all(self, _id: str):
    #     return self.run_query(
    #         """
    #         query fetch_by_id @cached {
    #                 dawn(where: {user_id: {_eq: """
    #         + _id
    #         + """ }}, order_by: {date: desc}) {
    #                     id
    #                     user_id
    #                     date
    #                     clock_in
    #                     clock_out
    #                 }
    #                 dusk(where: {user_id: {_eq: """
    #         + _id
    #         + """ }}, order_by: {date: desc}) {
    #                 id
    #                 user_id
    #                 date
    #                 clock_in
    #                 clock_out
    #                 }
    #             }
    #         """
    #     )
