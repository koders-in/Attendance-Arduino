from datetime import datetime, time, timedelta
from util import gql_fetch_user_attendance

# Morning shift starts from 02:00 AM
# Morning shift ends at 01:30 PM
# Evening Shift starts from 01:31 PM
# Evening Shift ends at 01:59 AM
# Cooldown interval should be of 30 minutes


def get_shift(_time: time):
    begin_time = time(2, 00)
    end_time = time(13, 30)
    if begin_time <= _time <= end_time:
        shift = "dawn"
    else:
        shift = "dusk"
    return shift


def is_cooldown(attendance_of_user: dict, shift: str):
    current_time = datetime.now().time()
    user_latest_time = None

    for key, value in attendance_of_user.items():
        if shift in key and value is not None:
            user_latest_time = value

    user_latest_time = datetime.strptime(user_latest_time, "%H:%M:%S").time()
    time_diff = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) - \
                timedelta(hours=user_latest_time.hour, minutes=user_latest_time.minute, seconds=user_latest_time.second)
    print(current_time)
    print(user_latest_time)
    if time_diff.total_seconds()/60 < 30:
        return True
    else:
        return False


def insert_attendance(user_id: str, _time: str):
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(current_date)
    print(_time)
    _time = datetime.strptime(_time, "%H:%M:%S").time()
    print(get_shift(_time))

    if get_shift(_time) == "dawn":
        # get user's latest attendance for current date
        attendance = gql_fetch_user_attendance(user_id=user_id, date=current_date)['attendance']
        if len(attendance) == 0:
            # first punch of the day
            # insert new entry for current date
            pass
        else:
            # second punch of the day
            if is_cooldown(attendance_of_user=attendance[0], shift="dawn"):
                return "cooldown period initiated. retry again after some time."
            else:
                # dawn clock out
                pass

    elif get_shift(_time) == "dusk":
        # get user's latest attendance for current date
        attendance = gql_fetch_user_attendance(user_id=user_id, date=current_date)['attendance']
        if len(attendance) != 0:
            # dusk clock out
            pass
        else:
            # dusk clock in by update attendance for current date
            pass


def get_attendance(user_id: str):
    return gql_fetch_user_attendance(user_id=user_id)
