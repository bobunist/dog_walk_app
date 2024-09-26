from datetime import time
from typing import Annotated

from pydantic import BeforeValidator


def validate_walk_time(walk_time: time | str) -> time:
    """
    Validate walk time.

    Time should be in format %H:%M:%S or %H:%M.
    Minutes should be equal 00 or 30.
    Time should be in range 07:00 to 23:00.
    Seconds should be equal 00.
    """
    if isinstance(walk_time, str):
        walk_time = time.fromisoformat(walk_time)
    if walk_time.minute not in (0, 30):
        raise ValueError("Invalid time format. Minutes should be equal 00 or 30.")
    if walk_time.second != 0:
        raise ValueError("Invalid time format. Seconds should be equal 00.")
    if not (time(7, 0) <= walk_time <= time(23, 0)):
        raise ValueError("Invalid time format. Use time between 07:00 and 23:00")
    return walk_time


WalkTime = Annotated[time, BeforeValidator(validate_walk_time)]
