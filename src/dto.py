from dataclasses import dataclass
from typing import List

from src.utils import convert_epoch_to_datetime, convert_datetime_to_timestamp


@dataclass
class Reading:
    # TODO: change this to represent whatever information is needed

    time: str
    name: str
    value: float

    @classmethod
    def create_reading(cls, parts: List[str]) -> "Reading":
        return Reading(
            time=convert_datetime_to_timestamp(
                convert_epoch_to_datetime(
                    int(parts[0])
                )
            ),
            name=str(parts[1]),
            value=float(parts[2])
        )
