from sqlalchemy.orm import Session
from app.controllers import report, store, business_hours
from app.utils.time_utils import is_within_business_hours, get_local_time
from datetime import datetime, timedelta
import pytz
import csv

def generate_report(report_id: str, db: Session):
    try:
        now = datetime.utcnow()
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)
        last_week = now - timedelta(weeks=1)

        stores = store.get_stores(db)
        report_data = []

        for store_data in stores:
            uptime_hour, downtime_hour = calculate_uptime_downtime(db, store_data.id, last_hour, now)
            uptime_day, downtime_day = calculate_uptime_downtime(db, store_data.id, last_day, now)
            uptime_week, downtime_week = calculate_uptime_downtime(db, store_data.id, last_week, now)

            report_data.append({
                "store_id": store_data.id,
                "uptime_last_hour": uptime_hour,
                "uptime_last_day": uptime_day / 60, 
                "uptime_last_week": uptime_week / 60,
                "downtime_last_hour": downtime_hour,
                "downtime_last_day": downtime_day / 60,
                "downtime_last_week": downtime_week / 60
            })

            file_name = 'output.csv'
            file_exists = False
            try:
                with open(file_name, 'r'):
                    file_exists = True
            except FileNotFoundError:
                file_exists = False

            with open(file_name, 'a', newline='') as csvfile:
                fieldnames = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 
                            'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                for data in report_data:
                    writer.writerow(data)

        report.update_report(db, report_id, "Complete")
    except Exception as e:
        print(f"Error generating report: {e}")
        report.update_report(db, report_id, "Error")

def calculate_uptime_downtime(db: Session, store_id: str, start_time: datetime, end_time: datetime):
    store_data = store.get_store(db, store_id)
    if not store_data:
        return 0, 0

    timezone = pytz.timezone(store_data.timezone_str)
    business_hours_data = business_hours.get_business_hours(db, store_id)
    statuses = store.get_store_status(db, store_id, start_time, end_time)
    uptime_minutes = 0
    downtime_minutes = 0
    last_status = None
    last_timestamp = None

    local_start = start_time.astimezone(timezone)
    local_end = end_time.astimezone(timezone)

    for status in statuses:
        local_time = get_local_time(status.timestamp_utc, timezone)
        if last_status is not None:
            time_diff = (local_time - last_timestamp).total_seconds() / 60

            if is_within_business_hours(last_timestamp, local_time, business_hours_data, timezone):
                if last_status == 'active':
                    uptime_minutes += time_diff
                else:
                    downtime_minutes += time_diff

        last_status = status.status
        last_timestamp = local_time

    if last_timestamp and last_timestamp < local_end:
        time_diff = (local_end - last_timestamp).total_seconds() / 60
        if is_within_business_hours(last_timestamp, local_end, business_hours_data, timezone):
            if last_status == 'active':
                uptime_minutes += time_diff
            else:
                downtime_minutes += time_diff

    return round(uptime_minutes), round(downtime_minutes)