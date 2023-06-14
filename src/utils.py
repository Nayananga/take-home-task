import time
from datetime import datetime
from datetime import date as Date


def convert_timestamp_to_epoch(date_str: str) -> int:
    # Convert date string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Convert datetime object to epoch time
    return int(date_obj.timestamp())


def convert_epoch_to_datetime(epoch: int) -> datetime:
    # Create a datetime object from the timestamp
    return datetime.fromtimestamp(epoch)


def convert_datetime_to_timestamp(dt: datetime) -> str:
    # Convert the datetime object to the desired string format
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def convert_date_to_epoch(date_obj: Date) -> int:
    # Convert date object to epoch time
    return int(time.mktime(date_obj.timetuple()))
