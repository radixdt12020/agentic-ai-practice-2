import re
from datetime import datetime

def is_leap_year(year: int) -> bool:
    if not isinstance(year, int):
        raise TypeError('Year must be an integer')
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def days_between(date1: str, date2: str) -> int:
    if not isinstance(date1, str) or not isinstance(date2, str):
        raise ValueError('Dates must be strings')
    
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not pattern.match(date1) or not pattern.match(date2):
        raise ValueError('Incorrect date format, must be YYYY-MM-DD')
    
    try:
        d1 = datetime.strptime(date1, '%Y-%m-%d').date()
        d2 = datetime.strptime(date2, '%Y-%m-%d').date()
    except ValueError as e:
        raise ValueError(f'Invalid date: {e}') from e
        
    return abs((d2 - d1).days)
