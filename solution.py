import re
from datetime import datetime


def is_leap_year(year: int) -> bool:
    """Determine whether a given year is a leap year based on Gregorian calendar rules."""
    if not isinstance(year, int) or isinstance(year, bool):
        raise TypeError("Year must be an integer")
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _parse_date(date_str: str):
    """Validate and parse 'YYYY-MM-DD' formatted date string."""
    if not isinstance(date_str, str):
        raise ValueError("Date must be a string in 'YYYY-MM-DD' format")
    
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError(f"Date '{date_str}' is not in the valid 'YYYY-MM-DD' format")
    
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date: {date_str}") from exc
    
    return parsed


def days_between(date1: str, date2: str) -> int:
    """Calculate the absolute number of days between two dates in 'YYYY-MM-DD' format."""
    d1 = _parse_date(date1)
    d2 = _parse_date(date2)
    return abs((d1 - d2).days)
