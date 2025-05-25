import time as _time
import datetime as _actual_datetime

from .helpers import _check_date_fields
from .constants import MINYEAR, NEPAL_TIME_UTC_OFFSET, REFERENCE_DATE_AD


class date:
    __slots__ = "_year", "_month", "_day", "_hashcode"

    def __new__(cls, year, month=None, day=None):
        year, month, day = _check_date_fields(int(year), int(month), int(day))
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        return self

    @classmethod
    def from_datetime_date(cls, from_date):
        if not isinstance(from_date, _actual_datetime.date):
            raise TypeError("Unsupported type {}.".format(type(from_date)))
        return cls(MINYEAR, 1, 1) + (
            from_date - _actual_datetime.date(**REFERENCE_DATE_AD)
        )

    @classmethod
    def fromtimestamp(cls, t):
        """Construct a date from a POSIX timestamp (like time.time())."""
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.gmtime(
            t + NEPAL_TIME_UTC_OFFSET
        )
        return cls.from_datetime_date(_actual_datetime.date(y, m, d))

    @classmethod
    def today(cls):
        """Construct a date from time.time()."""
        t = _time.time()
        return cls.fromtimestamp(t)

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    def isoformat(self):
        """Return the date formatted according to ISO.

        This is 'YYYY-MM-DD'.
        """
        return "%04d-%02d-%02d" % (self._year, self._month, self._day)

    __str__ = isoformat

    def __repr__(self):
        return "%s.%s(%d, %d, %d)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            self._year,
            self._month,
            self._day,
        )
