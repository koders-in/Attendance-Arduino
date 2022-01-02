from dataclasses import dataclass
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

    # Inserts clocked in time to db
    def post_time(self, _id: int, clock: str, day: str, table_name: str, status: str):
        self.run_query(
            """
        mutation ($_id: Int!, $clock: time!, $day: time!) {
            insert_""" + table_name + """_one(objects: {_id: $_id, """ + status + """: $clock, day: $day}) {
                affected_rows
                returning {
                    _id
                    """ + status + """
                    date
                }
            }
        }
        """,
            {'_id': _id, status: clock, day: day}
        )

    # Fetch clock_in or clock_out time for a given id
    def fetch_by_id(self, _id: int, table_name: str, status: str):
        return self.run_query(
            """
                query fetch_by_id($_id: Int!) {
                    """ + table_name + """_by_pk(_id: $_id) {
                        """ + status + """
                    }
                }
            """,
            {'_id': _id}
        )

    def query_for_all(self, _id: str):
        return self.run_query(
            """
            query fetch_by_id {
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


        # return self.run_query(
        #     """
        #         query fetch_by_id($_id: Int!) {
        #             """+table_name+"""_by_pk(_id: $_id) {
        #                 clock_in
        #                 clock_out
        #                 date
        #             }
        #         }
        #     """,
        #     {'_id': _id}
        # )
