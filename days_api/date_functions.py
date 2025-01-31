
"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Convert string to datetime obj"""
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError:
        raise ValueError('Unable to convert value to datetime.')


def get_days_between(first: datetime, last: datetime) -> int:
    """Get the number of days between two datetime objects"""
    try:
        diff = last - first
        return diff.days
    except TypeError:
        raise TypeError('Datetimes required.')


def get_day_of_week_on(date_val: datetime) -> str:
    """Get the day of week the input obj is on"""
    try:
        return date_val.strftime("%A")
    except AttributeError:
        raise TypeError("Datetime required.")


def get_current_age(birthdate: date) -> int:
    """Get the age of someone with input birthdate"""
    if not isinstance(birthdate, date):
        raise TypeError("Date required.")

    today = datetime.now()
    year_diff = today.year - birthdate.year
    if today.month < birthdate.month:
        year_diff -= 1
    elif today.month == birthdate.month and today.day < birthdate.day:
        year_diff -= 1
    return year_diff


if __name__ == '__main__':
    print(get_day_of_week_on(datetime.now()))
    print(get_current_age())
