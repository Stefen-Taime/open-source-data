"""Shared helper functions for random data generation."""

import random
import string
import uuid
from datetime import datetime


def random_uuid() -> str:
    """Return a new random UUID4 string."""
    return str(uuid.uuid4())


def random_number(length: int = 10) -> str:
    """Return a string of random digits of the given length."""
    return "".join(random.choice(string.digits) for _ in range(length))


def timestamp_now() -> str:
    """Return the current timestamp as 'YYYY-MM-DD HH:MM:SS'."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_today() -> str:
    """Return today's date as 'YYYYMMDD'."""
    return datetime.now().strftime("%Y%m%d")
