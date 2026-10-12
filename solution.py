import calendar
from datetime import date, datetime
from typing import Dict, Union


def is_leap_year(year: int) -> bool:
    """Determine whether a given year is a leap year."""
    if not isinstance(year, int) or isinstance(year, bool):
        raise TypeError("Year must be an integer")
    if year <= 0:
        raise ValueError("Year must be a positive integer")
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def is_valid_date(year: int, month: int, day: int) -> bool:
    """Validate if the given year, month, and day form a valid calendar date."""
    if not (isinstance(year, int) and isinstance(month, int) and isinstance(day, int)):
        return False
    if isinstance(year, bool) or isinstance(month, bool) or isinstance(day, bool):
        return False
    if year <= 0 or month < 1 or month > 12 or day < 1:
        return False
    try:
        date(year, month, day)
        return True
    except ValueError:
        return False


def days_in_month(year: int, month: int) -> int:
    """Return the number of days in a specific month of a specific year."""
    if not isinstance(year, int) or isinstance(year, bool):
        raise TypeError("Year must be an integer")
    if not isinstance(month, int) or isinstance(month, bool):
        raise TypeError("Month must be an integer")
    if year <= 0:
        raise ValueError("Year must be a positive integer")
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")
    return calendar.monthrange(year, month)[1]


def _parse_date(d: Union[str, date]) -> date:
    """Parse a date input (string YYYY-MM-DD or date object) into a datetime.date."""
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, date):
        return d
    if isinstance(d, str):
        try:
            return datetime.strptime(d.strip(), "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError(f"Invalid date string '{d}', expected format YYYY-MM-DD") from exc
    raise TypeError(f"Unsupported type for date: {type(d).__name__}. Expected str or datetime.date.")


def days_between(start_date: Union[str, date], end_date: Union[str, date], absolute: bool = False) -> int:
    """Calculate difference in days between two dates."""
    d1 = _parse_date(start_date)
    d2 = _parse_date(end_date)
    delta = (d2 - d1).days
    return abs(delta) if absolute else delta


def date_difference(start_date: Union[str, date], end_date: Union[str, date]) -> Dict[str, int]:
    """Return a detailed breakdown of the difference between two dates."""
    total_days = days_between(start_date, end_date, absolute=True)
    weeks = total_days // 7
    remaining_days = total_days % 7
    return {
        "days": total_days,
        "weeks": weeks,
        "remaining_days": remaining_days,
    }


class DateCalculator:
    """Encapsulates date difference calculations and leap year validation."""

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return is_leap_year(year)

    @staticmethod
    def is_valid_date(year: int, month: int, day: int) -> bool:
        return is_valid_date(year, month, day)

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        return days_in_month(year, month)

    @staticmethod
    def days_between(start_date: Union[str, date], end_date: Union[str, date], absolute: bool = False) -> int:
        return days_between(start_date, end_date, absolute=absolute)

    @staticmethod
    def difference(start_date: Union[str, date], end_date: Union[str, date]) -> Dict[str, int]:
        return date_difference(start_date, end_date)
