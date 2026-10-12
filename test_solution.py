from datetime import date, datetime
import pytest

from solution import (
    DateCalculator,
    date_difference,
    days_between,
    days_in_month,
    is_leap_year,
    is_valid_date,
)


class TestLeapYear:
    def test_typical_leap_years(self):
        assert is_leap_year(2020) is True
        assert is_leap_year(2024) is True
        assert is_leap_year(2028) is True

    def test_typical_non_leap_years(self):
        assert is_leap_year(2021) is False
        assert is_leap_year(2022) is False
        assert is_leap_year(2023) is False

    def test_century_years(self):
        assert is_leap_year(2000) is True
        assert is_leap_year(1600) is True
        assert is_leap_year(2400) is True
        assert is_leap_year(1900) is False
        assert is_leap_year(1800) is False
        assert is_leap_year(2100) is False

    def test_invalid_types_and_values(self):
        with pytest.raises(ValueError):
            is_leap_year(0)
        with pytest.raises(ValueError):
            is_leap_year(-2020)
        with pytest.raises(TypeError):
            is_leap_year(2020.5)  # type: ignore
        with pytest.raises(TypeError):
            is_leap_year("2020")  # type: ignore
        with pytest.raises(TypeError):
            is_leap_year(True)  # type: ignore


class TestDaysInMonth:
    def test_february_leap_and_non_leap(self):
        assert days_in_month(2024, 2) == 29
        assert days_in_month(2023, 2) == 28
        assert days_in_month(2000, 2) == 29
        assert days_in_month(1900, 2) == 28

    def test_standard_months(self):
        assert days_in_month(2023, 1) == 31
        assert days_in_month(2023, 4) == 30
        assert days_in_month(2023, 7) == 31
        assert days_in_month(2023, 8) == 31

    def test_invalid_month(self):
        with pytest.raises(ValueError):
            days_in_month(2023, 0)
        with pytest.raises(ValueError):
            days_in_month(2023, 13)
        with pytest.raises(TypeError):
            days_in_month(2023, "1")  # type: ignore


class TestIsValidDate:
    def test_valid_dates(self):
        assert is_valid_date(2024, 2, 29) is True
        assert is_valid_date(2023, 12, 31) is True
        assert is_valid_date(2023, 4, 30) is True

    def test_invalid_dates(self):
        assert is_valid_date(2023, 2, 29) is False
        assert is_valid_date(2023, 4, 31) is False
        assert is_valid_date(2023, 13, 1) is False
        assert is_valid_date(-2023, 1, 1) is False
        assert is_valid_date(2023, 1, 32) is False
        assert is_valid_date("2023", 1, 1) is False  # type: ignore


class TestDaysBetween:
    def test_same_date(self):
        assert days_between("2023-01-01", "2023-01-01") == 0
        assert days_between(date(2023, 1, 1), date(2023, 1, 1)) == 0

    def test_signed_and_absolute_difference(self):
        assert days_between("2023-01-01", "2023-01-10") == 9
        assert days_between("2023-01-10", "2023-01-01") == -9
        assert days_between("2023-01-10", "2023-01-01", absolute=True) == 9

    def test_across_month_and_year_boundary(self):
        assert days_between("2023-12-30", "2024-01-02") == 3
        # Crossing leap day 2024-02-29
        assert days_between("2024-02-28", "2024-03-01") == 2
        # Non-leap year
        assert days_between("2023-02-28", "2023-03-01") == 1

    def test_datetime_object_support(self):
        dt1 = datetime(2023, 5, 1, 10, 30)
        dt2 = datetime(2023, 5, 5, 15, 45)
        assert days_between(dt1, dt2) == 4

    def test_invalid_date_inputs(self):
        with pytest.raises(ValueError):
            days_between("invalid-date", "2023-01-01")
        with pytest.raises(ValueError):
            days_between("2023-02-30", "2023-03-01")
        with pytest.raises(TypeError):
            days_between(12345, "2023-01-01")  # type: ignore


class TestDateDifferenceBreakdown:
    def test_difference_breakdown(self):
        diff = date_difference("2023-01-01", "2023-01-17")
        assert diff["days"] == 16
        assert diff["weeks"] == 2
        assert diff["remaining_days"] == 2

    def test_difference_reverse_order(self):
        diff = date_difference("2023-01-17", "2023-01-01")
        assert diff["days"] == 16
        assert diff["weeks"] == 2
        assert diff["remaining_days"] == 2


class TestDateCalculatorClass:
    def test_class_wrapper_methods(self):
        calc = DateCalculator()
        assert calc.is_leap_year(2024) is True
        assert calc.is_valid_date(2024, 2, 29) is True
        assert calc.days_in_month(2024, 2) == 29
        assert calc.days_between("2024-01-01", "2024-01-05") == 4
        diff = calc.difference("2024-01-01", "2024-01-10")
        assert diff["days"] == 9
