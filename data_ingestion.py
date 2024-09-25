import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.database import get_db, Store, StoreStatus, BusinessHours

def ingest_data(file_path, model, row_model):
    db = get_db()
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            batch=[]
            for row in reader:
                data = row_model(row)
                batch.append(data)
                if len(batch) >= 1000:
                    db.bulk_save_objects(batch)
                    db.commit()
                    batch = []
            if batch:
                db.bulk_save_objects(batch)
                db.commit()
    finally:
        db.close()

def row_to_store_status(row):
    return StoreStatus(
        store_id=row['store_id'],
        timestamp_utc=datetime.fromisoformat(row['timestamp_utc'].replace(' UTC', 'Z')),
        status=row['status']
    )

def row_to_business_hours(row):
    return BusinessHours(
        store_id=row['store_id'],
        day_of_week=int(row['day']),
        start_time_local=row['start_time_local'],
        end_time_local=row['end_time_local']
    )

def row_to_store(row):
    return Store(
        id=row['store_id'],
        timezone_str=row['timezone_str']
    )

def ingest_all_data(status_file: str, hours_file: str, timezone_file: str):
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(ingest_data, status_file, StoreStatus, row_to_store_status),
            executor.submit(ingest_data, hours_file, BusinessHours, row_to_business_hours),
            executor.submit(ingest_data, timezone_file, Store, row_to_store)
        ]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    hours_file = "business_hours.csv"
    status_file = "store_status.csv"
    timezones_file = "timezones.csv"

    ingest_all_data(status_file, hours_file, timezones_file)