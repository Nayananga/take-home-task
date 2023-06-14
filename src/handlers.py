from copy import deepcopy
from typing import Dict, List

from flask import request, Request

from src.db import get_all_keys, get_reading, add_reading
from src.dto import Reading
from src.utils import convert_epoch_to_datetime


def prepare_data(start_key: int, end_key: int) -> Dict:
    keys_in_range = [key for key in get_all_keys() if start_key <= key <= end_key]

    all_data: Dict[int, Dict[str, Reading | None]] = {
        key: get_reading(str(key)) for key in keys_in_range
    }

    all_data_by_date = get_all_data_by_date(all_data)

    avg_pwr_data_by_date = get_avg_data_by_date(all_data_by_date)

    all_data_output = []

    for d in all_data.values():
        all_data_output.extend(d.values())

    output = {
        "all_data": all_data_output,
        "avg data": avg_pwr_data_by_date
    }

    return output


def get_avg_data_by_date(all_data_by_date: Dict[str, Dict[str, List[float]]]) -> Dict[str, Dict[str, float]]:
    avg_pwr_data_by_date: Dict[str, Dict[str, float]] = {}
    avg_value_data: Dict[str, float] = {}
    for d, data in all_data_by_date.items():
        avg_pwr_data_by_date[d] = deepcopy(avg_value_data)

        for name, values in data.items():
            avg_pwr_data_by_date[d][name] = (
                sum(values) / len(values)
                if len(values) else "N/A"
            )

    return avg_pwr_data_by_date


def get_all_data_by_date(all_data: Dict[int, Dict[str, Reading | None]]) -> Dict[str, Dict[str, List[float]]]:
    # Convert epochs to datetime objects and group by day
    all_data_by_date: Dict[str, Dict[str, List[float]]] = {}
    value_data: Dict[str, List[float]] = {}
    for epoch, readings in all_data.items():
        dt = convert_epoch_to_datetime(epoch)
        date = dt.date()
        date_str = date.isoformat()

        if date_str not in all_data_by_date:
            all_data_by_date[date_str] = deepcopy(value_data)
        for name, reading in readings.items():
            try:
                all_data_by_date[date_str][name].append(reading.value)
            except KeyError:
                all_data_by_date[date_str][name] = [reading.value]

    return all_data_by_date


def save_data(req: Request) -> None:
    data = req.data.decode('utf-8')  # Decode the raw data from the request
    lines = data.split('\n')  # Split the data into lines
    for line in lines:
        parts = line.strip().split(' ')
        record = Reading.create_reading(parts)
        add_reading(
            parts[0],
            record
        )
