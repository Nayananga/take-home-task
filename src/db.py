from typing import List

from src.dto import Reading

# This is a fake database which stores data in-memory while the process is running
# Feel free to change the data structure to anything else you would like
database: dict[str, dict[str, Reading | None]] = {}


def add_reading(key: str, reading: Reading) -> None:
    """
    Store a reading in the database using the given key
    """
    if key not in database:
        database[key] = {}
    database[key][reading.name] = reading


def get_reading(key: str) -> dict[str, Reading | None]:
    """
    Retrieve a reading from the database using the given key
    """
    return database.get(key, None)


def get_all_keys() -> List[int]:
    """
    Retrieve all reading keys from the database
    """
    return [int(key) for key in database.keys()]
