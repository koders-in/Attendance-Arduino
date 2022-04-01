import os

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


client = Client(
    transport=AIOHTTPTransport(
        url=os.getenv('HASURA_URL'),
        headers={"X-Hasura-Admin-Secret": os.getenv("SECRET_KEY")}
    ),
    fetch_schema_from_transport=True
)


# date str format: YYYY-MM-DD
# time str format: HH:MM:SS

def gql_fetch_user_attendance(user_id: int, offset: int = 0, date: str = None):
    """
    GQL query to fetch user's all records for attendance or for a particular date

    :param user_id: unique user id
    :param offset: no. of records to skip (from start)
    :param date: date string in YYYY-MM-DD format
    :return: GQL result dict
    """
    if date is None:
        # get all data for user if no date is provided
        # TODO => add offset
        query = gql(
            '''
            query getData($user_id: Int!, $offset: Int!) @cached {
                attendance(where: {user_id: {_eq: $user_id}}, limit: 10, offset: $offset) {
                    id
                    date
                    user_id
                    clock_in
                    clock_out
                    comment
                }
            }
            '''
        )
        variables = {
            "user_id": user_id,
            "offset": offset
        }
    else:
        # get data for specific date
        query = gql(
            '''
            query getData($user_id: Int!, $date: date!) @cached {
                attendance(where: {user_id: {_eq: $user_id}, date: {_eq: $date}}, limit: 1, order_by: {id: desc}) {
                    id
                    date
                    user_id
                    clock_in
                    clock_out
                    comment
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


def gql_add_user_attendance(time: str, user_id: int = None, date: str = None, attendance_id: int = None,
                            is_clock_in: bool = True, comment: str = None):
    """
    GQL mutation to insert/update attendance
    :param time: time string in HH:MM:SS format
    :param user_id: unique user id
    :param date: date string in YYYY-MM-DD format
    :param attendance_id: unique attendance id
    :param is_clock_in: toggle for insert attendance (clock_in) or update attendance (clock_out), default True i.e. insert attendance
    :param comment: comment on attendance record
    :return: GQL result dict
    """
    if is_clock_in:
        # attendance clock in => create new record
        if user_id is None or date is None or time is None:
            return "ERROR: arguments missing, user_id, date and time are required."

        query = gql(
            '''
            mutation addNewAttendance($user_id: Int!, $time: time!, $date: date!, $comment: String) {
                insert_attendance_one(object: {clock_in: $time, user_id: $user_id, date: $date, comment: $comment}) {
                    id
                    user_id
                    date
                }
            }
            '''
        )

        variables = {
            "user_id": user_id,
            "date": date,
            "time": time,
            "comment": comment
        }
    else:
        # attendance clock out => update existing record using attendance record id
        if attendance_id is None or time is None:
            return "ERROR: arguments missing, attendance_id and time are required."

        query = gql(
            '''
            mutation updateAttendance($id: Int!, $time: time!, $comment: String) {
                update_attendance_by_pk(pk_columns: {id: $id}, _set: {clock_out: $time, comment: $comment}) {
                    id
                    user_id
                    date
                }
            }
            '''
        )

        variables = {
            "id": attendance_id,
            "time": time,
            "comment": comment
        }

    try:
        result = client.execute(query, variable_values=variables)
        return result
    except Exception as error:
        return error
