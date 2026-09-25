from datetime import datetime, timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from meteoscope.services.observation_datetime import is_complete_day

PARIS = ZoneInfo("Europe/Paris")


def make_observation(timestamp: datetime) -> SimpleNamespace:
    return SimpleNamespace(timestamp=timestamp)


def make_hourly_observations(
    start_datetime: datetime,
    end_datetime: datetime,
) -> list[SimpleNamespace]:
    start_utc = start_datetime.astimezone(ZoneInfo("UTC"))
    end_utc = end_datetime.astimezone(ZoneInfo("UTC"))

    observations = []
    current_datetime = start_utc

    while current_datetime < end_utc:
        observations.append(make_observation(current_datetime))
        current_datetime += timedelta(hours=1)

    return observations


def test_is_complete_day_with_24_hours() -> None:
    start = datetime(2026, 9, 17, 0, 0, tzinfo=PARIS)
    end = datetime(2026, 9, 18, 0, 0, tzinfo=PARIS)

    observations = make_hourly_observations(start, end)

    assert len(observations) == 24
    assert is_complete_day(
        observations,
        start,
        end,
    )


def test_is_complete_day_returns_false_when_observation_is_missing() -> None:
    start = datetime(2026, 9, 17, 0, 0, tzinfo=PARIS)
    end = datetime(2026, 9, 18, 0, 0, tzinfo=PARIS)

    observations = make_hourly_observations(start, end)
    observations.pop(12)

    assert len(observations) == 23
    assert not is_complete_day(
        observations,
        start,
        end,
    )


def test_is_complete_day_with_23_hours_dst_start() -> None:
    start = datetime(2026, 3, 29, 0, 0, tzinfo=PARIS)
    end = datetime(2026, 3, 30, 0, 0, tzinfo=PARIS)

    observations = make_hourly_observations(start, end)

    assert len(observations) == 23
    assert is_complete_day(
        observations,
        start,
        end,
    )


def test_is_complete_day_with_25_hours_dst_end() -> None:
    start = datetime(2026, 10, 25, 0, 0, tzinfo=PARIS)
    end = datetime(2026, 10, 26, 0, 0, tzinfo=PARIS)

    observations = make_hourly_observations(start, end)

    assert len(observations) == 25
    assert is_complete_day(
        observations,
        start,
        end,
    )


def test_is_incomplete_day_with_24_hours_dst_end() -> None:
    start = datetime(2026, 10, 25, 0, 0, tzinfo=PARIS)
    end = datetime(2026, 10, 26, 0, 0, tzinfo=PARIS)

    timestamps = [
        datetime(2026, 9, 17, 0, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 1, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 2, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 3, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 4, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 5, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 6, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 7, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 8, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 9, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 10, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 11, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 13, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 13, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 14, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 15, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 16, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 17, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 18, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 19, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 20, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 21, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 22, 0, tzinfo=PARIS),
        datetime(2026, 9, 17, 23, 0, tzinfo=PARIS),
    ]
    observations = [make_observation(ts) for ts in timestamps]

    assert len(observations) == 24
    assert not is_complete_day(
        observations,
        start,
        end,
    )
