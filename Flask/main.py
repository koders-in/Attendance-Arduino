from datetime import datetime, timedelta
from util import gql_fetch_user_attendance, gql_add_user_attendance
from embeds import send_webhook

COOLDOWN_INTERVAL = 30  # in minutes


def is_cooldown(attendance_of_user: dict):
    """
    Helper function to check cooldown status

    :param attendance_of_user: dict of user record of a particular date
    :return: cooldown status, True or False
    """
    current_time = datetime.now().time()
    user_latest_time = None

    # check for latest time entry in record
    for key, value in attendance_of_user.items():
        if 'clock' in key and value is not None:
            user_latest_time = value

    user_latest_time = datetime.strptime(user_latest_time, "%H:%M:%S").time()
    # calculate time diff
    time_diff = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) - \
                timedelta(hours=user_latest_time.hour, minutes=user_latest_time.minute, seconds=user_latest_time.second)

    if time_diff.total_seconds()/60 < COOLDOWN_INTERVAL:
        return True
    else:
        return False


def insert_attendance(user_id: str, _time: str):
    """
    Post/Update user's attendance
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    attendance = gql_fetch_user_attendance(user_id=int(user_id), date=current_date)['attendance']
    if len(attendance) == 0:
        # new record for current date
        send_webhook(int(user_id), 'green')
        return gql_add_user_attendance(user_id=int(user_id), time=_time, date=current_date)
    else:
        # existing attendance record
        record = attendance[0]
        if record['clock_out'] is None:
            # update clock out
            if is_cooldown(record):
                return "cooldown initiated. try again later."
            send_webhook(int(user_id), 'red')
            return gql_add_user_attendance(is_clock_in=False, attendance_id=record['id'], time=_time)
        else:
            # new record for same day => clock in
            if is_cooldown(record):
                return "cooldown initiated. try again later."
            send_webhook(int(user_id), 'green')
            return gql_add_user_attendance(user_id=int(user_id), time=_time, date=current_date)


def get_attendance(user_id: str, offset: int):
    """
    Get attendance record for a particular user.
    TODO => Add offset fetching
    """
    return gql_fetch_user_attendance(user_id=int(user_id), offset=offset)
