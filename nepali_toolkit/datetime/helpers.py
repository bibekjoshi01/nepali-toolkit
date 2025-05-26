import os
import json

from .constants import MINYEAR, MAXYEAR


def _index(a):
    "Same as a.__index__()."
    return a.__index__()


_CALENDAR = {}

_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(_dir, "data", "calender.json"), encoding="utf-8") as f:
    _CALENDAR = json.load(f)


def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, f"Invalid month: {month}"
    return _CALENDAR[str(year)]["months"][str(month)]


def _check_date_fields(year, month, day):
    year = _index(year)
    month = _index(month)
    day = _index(day)

    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError("year must be in %d..%d" % (MINYEAR, MAXYEAR), year)

    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12", month)

    dim = _days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError("day must be in 1..%d" % dim, day)

    return year, month, day


def _compare(x, y):
    return 0 if x == y else 1 if x > y else -1