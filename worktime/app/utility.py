# Built-in Modules
from datetime import date, datetime, timedelta
from os import name, system

# Third-party Package
import pytz


# Source: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    """Clear the screen."""
    system("cls" if name == "nt" else "clear")


def get_current_datetime():
    """Get the current datetime of Dublin.

    Returns:
        dict: The current year, date and time of Dublin.
    """
    DUBLIN = pytz.timezone("Europe/Dublin")
    now = datetime.now(DUBLIN)
    date = now.date().strftime("%d/%m/%Y")
    time = now.time().strftime("%H:%M:%S")
    return {"year": now.year, "date": date, "time": time}


def get_today():
    """Get the current date of Dublin.

    Returns:
        date: A instans of datetime.date().
    """
    DUBLIN = pytz.timezone("Europe/Dublin")
    return datetime.now(DUBLIN).date()


def get_week(xdate, result):
    """Return a list of a week(inc./excl. weekend) of the given date.

    Args:
        xdate date: An instance of datetime.date().
        result str: Including or excluding weekend.

    Returns
        list: Dates of a week.
    """
    # Source: ALFAFA's answer on Stack Overflow
    # https://stackoverflow.com/questions/56163008
    week = xdate.isocalendar()[2]
    start = xdate - timedelta(days=week)
    dates = []
    if result == "weekdays":
        for day in range(1, 6):
            dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    else:
        for day in range(1, 8):
            dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    return dates


def convert_date(xdate):
    """Split a string into a list of integers that represet
    year, month and date, and then pass them to date() object.

    Args:
        xdate str: A date - DD/MM/YYYY.

    Returns:
        date: An instans of datetime.date().
    """
    date_to_list = xdate.split("/")
    year = int(date_to_list[2])
    month = int(date_to_list[1])
    day = int(date_to_list[0])
    return date(year, month, day)


def get_num_of_weekdays(date1, date2):
    """Calculate total number of weekdays between two dates.

    Args:
        date1 str: Start date - DD/MM/YYYY.
        date2 str: End date - DD/MM/YYYY.

    Returns:
        int: Total number of weekdays.
    """
    # Source: Dave Webb's answer on Stack Overflow
    # https://stackoverflow.com/questions/3615375
    date1 = convert_date(date1)
    date2 = convert_date(date2)
    days = (date1 + timedelta(n) for n in range((date2 - date1).days + 1))
    total_weekdays = sum(1 for day in days if day.weekday() < 5)
    return total_weekdays
