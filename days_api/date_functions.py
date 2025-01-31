"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError:
        raise ValueError('Unable to convert value to datetime.')


def get_days_between(first: datetime, last: datetime) -> int:
    try:
        diff = last - first
        return diff.days
    except TypeError:
        raise TypeError('Datetimes required.')


def get_day_of_week_on(date_val: datetime) -> str:
    pass


def get_current_age(birthdate: date) -> int:
    pass


if __name__ == '__main__':
    get_days_between('31.02.2013', '17:10:2002')
