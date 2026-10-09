import pytest
from solution import is_leap_year, days_between

def test_is_leap_year():
    # Divisible by 4, not 100
    assert is_leap_year(2024) is True
    assert is_leap_year(2016) is True
    
    # Divisible by 100, not 400
    assert is_leap_year(1900) is False
    assert is_leap_year(2100) is False
    
    # Divisible by 400
    assert is_leap_year(2000) is True
    assert is_leap_year(1600) is True
    
    # Not divisible by 4
    assert is_leap_year(2023) is False
    assert is_leap_year(2025) is False

def test_is_leap_year_type_error():
    with pytest.raises(TypeError):
        is_leap_year('2024')  # type: ignore

def test_days_between_valid():
    assert days_between('2023-01-01', '2023-01-01') == 0
    assert days_between('2023-01-01', '2023-01-02') == 1
    assert days_between('2023-01-02', '2023-01-01') == 1
    
    # Leap year checking
    assert days_between('2024-02-28', '2024-03-01') == 2  # 2024-02-29 exists
    assert days_between('2023-02-28', '2023-03-01') == 1  # 2023-02-29 doesn't exist
    
    # Span across years
    assert days_between('2019-12-31', '2021-01-01') == 367  # 2020 is leap year

def test_days_between_invalid_formats():
    invalid_formats = [
        '2023/01/01',
        '2023-1-1',
        '23-01-01',
        '2023-01-01 extra',
        'extra 2023-01-01',
        '2023-01-01\n',
        'YYYY-MM-DD',
        '',
    ]
    for val in invalid_formats:
        with pytest.raises(ValueError):
            days_between(val, '2023-01-01')
        with pytest.raises(ValueError):
            days_between('2023-01-01', val)

def test_days_between_invalid_dates():
    invalid_dates = [
        '2023-02-29',  # 2023 is not leap
        '2024-02-30',  # February has max 29 days
        '2023-04-31',  # April has 30 days
        '2023-13-01',  # 13th month
        '2023-00-01',  # 0th month
        '2023-01-00',  # 0th day
        '2023-01-32',  # 32nd day
    ]
    for val in invalid_dates:
        with pytest.raises(ValueError):
            days_between(val, '2023-01-01')
        with pytest.raises(ValueError):
            days_between('2023-01-01', val)

def test_days_between_invalid_types():
    with pytest.raises(ValueError):
        days_between(123, '2023-01-01')  # type: ignore
    with pytest.raises(ValueError):
        days_between('2023-01-01', None)  # type: ignore
