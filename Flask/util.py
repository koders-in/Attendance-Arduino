import os
from dotenv import load_dotenv

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


load_dotenv()   # env file is in the same dir /Flask/.env
client = Client(
    transport=AIOHTTPTransport(
        url=os.getenv('HASURA_URL'),
        headers={"X-Hasura-Admin-Secret": os.getenv("SECRET_KEY")}
    ),
    fetch_schema_from_transport=True
)


# date str format: YYYY-MM-DD
# time str format: HH:MM:SS

def gql_fetch_user_attendance(user_id: str, date: str = None):
    if date is None:
        # get all data for user if no date is provided
        query = gql(
            '''
            query getData($user_id: String!) {
                attendance(where: {user_id: {_eq: $user_id}}) {
                    date
                    dawn_clock_in
                    dawn_clock_out
                    dusk_clock_in
                    dusk_clock_out
                    _id
                    user_id
                }
            }
            '''
        )
        variables = {
            "user_id": user_id
        }
    else:
        # get data for specific date
        query = gql(
            '''
            query getData($user_id: String!, $date: date!) {
                attendance(where: {user_id: {_eq: $user_id}, date: {_eq: $date}}) {
                    date
                    dawn_clock_in
                    dawn_clock_out
                    dusk_clock_in
                    dusk_clock_out
                    _id
                    user_id
                }
            }
            '''
        )

        variables = {
            "user_id": user_id,
            "date": date
        }

    try:
        result = client.execute(query, variable_values=variables)
        return result
    except Exception as error:
        return error


def gql_add_user_attendance(user_id: str, date: str, shift: str, time: str):
    query = gql(
        '''
        mutation addData($date: date!, $time: time!, $user_id: String!) {
            insert_attendance_one(object: {date: $date, '''+shift+'''_clock_in: $time, user_id: $user_id}) {
                _id
            }
        }
        '''
    )

    variables = {
        "user_id": user_id,
        "date": date,
        "time": time
    }

    try:
        result = client.execute(query, variable_values=variables)
        return result
    except Exception as error:
        return error


def gql_update_user_attendance(user_id: str, date: str, shift: str, time: str):

    if shift == "dusk":
        # query -> clock out dawn if dawn clock in exists + clock in dusk
        pass
    elif shift == "dawn":
        # query -> clock out dusk if dusk clock in exists + clock in dawn
        pass

    query = gql(
        '''
        '''
    )

    variables = {
        "user_id": user_id,
        "date": date,
        "time": time
    }

    try:
        result = client.execute(query, variable_values=variables)
        return result
    except Exception as error:
        return error
