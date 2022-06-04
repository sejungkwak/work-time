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
    """Return the current date and time in Dublin in a dictionary."""
    DUBLIN = pytz.timezone("Europe/Dublin")
    now = datetime.now(DUBLIN)
    date = now.date().strftime("%d/%m/%Y")
    time = now.time().strftime("%H:%M:%S")
    return {"year": now.year, "date": date, "time": time}


def get_week(data, result):
    """Return a list of a week(inc./excl. weekend) of the given date.

    Args:
        :data class: An instance of datetime.date.
        :result str: Including or excluding weekend
    """
    # Source: ALFAFA's answer on Stack Overflow
    # https://stackoverflow.com/questions/56163008
    week = data.isocalendar()[2]
    start = data - timedelta(days=week)
    dates = []
    if result == "weekdays":
        for day in range(1, 6):
            dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    else:
        for day in range(7):
            dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    return dates


def convert_date(data):
    """Convert a date to an instance of datetime.date.

    Args:
        :data str: A day/month/year formatted date.
    """
    date_to_list = data.split("/")
    year = int(date_to_list[2])
    month = int(date_to_list[1])
    day = int(date_to_list[0])
    return date(year, month, day)
