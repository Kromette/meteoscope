from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from typing import Protocol


class ObservationWithTimestamp(Protocol):
    timestamp: datetime


def is_complete_day(
    observations: Sequence[ObservationWithTimestamp],
    start_datetime: datetime,
    end_datetime: datetime,
) -> bool:
    start_utc = start_datetime.astimezone(UTC)
    end_utc = end_datetime.astimezone(UTC)

    expected_timestamps = set()
    current_datetime = start_utc

    while current_datetime < end_utc:
        expected_timestamps.add(current_datetime)
        current_datetime += timedelta(hours=1)

    actual_timestamps = {obs.timestamp.astimezone(UTC) for obs in observations}

    return expected_timestamps == actual_timestamps
