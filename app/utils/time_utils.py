from datetime import datetime, timedelta
import pytz

def convert_to_utc(timezone_str:str, local_time:str):
    local_tz = pytz.timezone(timezone_str)
    local_datetime = datetime.strptime(local_time, "%H:%M:%S")
    local_dt = local_tz.localize(local_datetime)
    return local_dt.astimezone(pytz.UTC)

def is_within_business_hours(start: datetime, end: datetime, business_hours, timezone: pytz.timezone) -> bool:
    current = start
    while current <= end:
        local_time = get_local_time(current, timezone)
        day_of_week = local_time.weekday()
        time = local_time.time()

        for hours in business_hours:
            if hours.day_of_week == day_of_week:
                start_time = datetime.strptime(hours.start_time_local, "%H:%M:%S").time()
                end_time = datetime.strptime(hours.end_time_local, "%H:%M:%S").time()
                if start_time <= time <= end_time:
                    return True

        current += timedelta(minutes=1)
    return False

def get_local_time(timestamp: datetime, timezone: pytz.timezone) -> datetime:
    return timestamp.astimezone(timezone)