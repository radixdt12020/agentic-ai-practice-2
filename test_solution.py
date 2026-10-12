import pytest
from solution import is_leap_year, days_between


class TestIsLeapYear:
    @pytest.mark.parametrize(
        "year",
        [1600, 2000, 2400, 400, 800, 1200],
    )
    def test_divisible_by_400_is_leap_year(self, year):
        assert is_leap_year(year) is True

    @pytest.mark.parametrize(
        "year",
        [1700, 1800, 1900, 2100, 2200, 2300, 2500],
    )
    def test_divisible_by_100_not_400_is_not_leap_year(self, year):
        assert is_leap_year(year) is False

    @pytest.mark.parametrize(
        "year",
        [2004, 2008, 2012, 2016, 2020, 2024, 2028],
    )
    def test_divisible_by_4_not_100_is_leap_year(self, year):
        assert is_leap_year(year) is True

    @pytest.mark.parametrize(
        "year",
        [2001, 2002, 2003, 2019, 2021, 2022, 2023],
    )
    def test_not_divisible_by_4_is_not_leap_year(self, year):
        assert is_leap_year(year) is False

    @pytest.mark.parametrize(
        "invalid_input",
        ["2020", 2020.0, None, [2020], True, False],
    )
    def test_invalid_type_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            is_leap_year(invalid_input)


class TestDaysBetweenValid:
    def test_same_date(self):
        assert days_between("2023-01-01", "2023-01-01") == 0

    def test_consecutive_days(self):
        assert days_between("2023-01-01", "2023-01-02") == 1
        assert days_between("2023-01-02", "2023-01-01") == 1

    def test_non_leap_year_february_to_march(self):
        assert days_between("2023-02-28", "2023-03-01") == 1

    def test_leap_year_february_to_march(self):
        assert days_between("2024-02-28", "2024-03-01") == 2
        assert days_between("2024-02-28", "2024-02-29") == 1
        assert days_between("2024-02-29", "2024-03-01") == 1

    def test_full_year_non_leap(self):
        assert days_between("2023-01-01", "2024-01-01") == 365

    def test_full_year_leap(self):
        assert days_between("2024-01-01", "2025-01-01") == 366

    def test_century_boundary(self):
        assert days_between("1999-12-31", "2000-01-01") == 1
        assert days_between("2000-01-01", "2001-01-01") == 366

    def test_multiple_years(self):
        # 2020 is leap (366), 2021 is non-leap (365) => 731 days
        assert days_between("2020-01-01", "2022-01-01") == 731


class TestDaysBetweenInvalid:
    @pytest.mark.parametrize(
        "invalid_date",
        [
            "2023-02-29",  # Not a leap year
            "2021-02-29",  # Not a leap year
            "1900-02-29",  # 1900 is not a leap year
            "2024-02-30",  # Leap year February only has 29 days
            "2023-04-31",  # April only has 30 days
            "2023-06-31",  # June only has 30 days
            "2023-09-31",  # September only has 30 days
            "2023-11-31",  # November only has 30 days
            "2023-13-01",  # Invalid month
            "2023-00-01",  # Invalid month
            "2023-01-00",  # Invalid day
            "2023-01-32",  # Invalid day
        ],
    )
    def test_invalid_calendar_dates(self, invalid_date):
        with pytest.raises(ValueError):
            days_between(invalid_date, "2023-01-01")
        with pytest.raises(ValueError):
            days_between("2023-01-01", invalid_date)

    @pytest.mark.parametrize(
        "malformed_date",
        [
            "2023/01/01",       # Wrong separator
            "01-01-2023",       # Wrong component order
            "2023-1-01",        # Month not zero-padded
            "2023-01-1",        # Day not zero-padded
            "23-01-01",         # 2-digit year
            "2023-01-01T00:00", # ISO with time
            "2023-01-01 ",      # Trailing space
            " 2023-01-01",      # Leading space
            "not-a-date",       # Letters
            "",                 # Empty string
            "20230101",         # No separator
        ],
    )
    def test_malformed_formats(self, malformed_date):
        with pytest.raises(ValueError):
            days_between(malformed_date, "2023-01-01")
        with pytest.raises(ValueError):
            days_between("2023-01-01", malformed_date)

    @pytest.mark.parametrize(
        "non_str",
        [None, 12345, True, ["2023-01-01"]],
    )
    def test_non_string_types(self, non_str):
        with pytest.raises(ValueError):
            days_between(non_str, "2023-01-01")
        with pytest.raises(ValueError):
            days_between("2023-01-01", non_str)
