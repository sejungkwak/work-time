# Built-in Modules
from datetime import date, datetime, timedelta
from os import name, system

# Third-party Package
import pytz


# Source: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    """Clear the screen."""
    system("cls" if name == "nt" else "clear")


def get_datetime():
    """Return the current date and time in Dublin in a dictionary."""
    DUBLIN = pytz.timezone("Europe/Dublin")
    now = datetime.now(DUBLIN)
    date = now.date().strftime("%d/%m/%Y")
    time = now.time().strftime("%H:%M:%S")
    return {"year": now.year, "date": date, "time": time}


def get_week(year, month, day):
    """Return a list of weekdays of the given date."""
    # Source: ALFAFA's answer on Stack Overflow
    # https://stackoverflow.com/questions/56163008
    target_date = date(year, month, day)
    week = target_date.isocalendar()[2]
    start = target_date - timedelta(days=week)
    dates = []
    for day in range(1, 6):
        dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    return dates
