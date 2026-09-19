import os

from dotenv import load_dotenv

load_dotenv()


def get_float_env(name: str) -> float:
    value = os.environ.get(name)

    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")

    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be a number.") from exc


def get_required_env(name: str) -> str:
    value = os.environ.get(name)

    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


METEOSCOPE_LATITUDE = get_float_env("METEOSCOPE_LATITUDE")
METEOSCOPE_LONGITUDE = get_float_env("METEOSCOPE_LONGITUDE")
METEOSCOPE_TIMEZONE = get_required_env("METEOSCOPE_TIMEZONE")
