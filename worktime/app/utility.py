"""Utility module

This module provides functions for clearing the console, changing
text colour, getting and converting a date and time and displaying a table.
"""

# Built-in Modules
from datetime import date, datetime, time, timedelta
from enum import Enum
from os import name, system

# Third-party Packages
from colorama import init, Back, Fore, Style
import pytz
from tabulate import tabulate

# colorama method to enable it on Windows
init()


# Source: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    """Clear the screen."""
    system("cls" if name == "nt" else "clear")


class Colours(Enum):
    """Represent collection of colorama font or background colours."""
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Back.RED
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL


def print_in_colour(colour, text):
    """Print the text in a different colour.

    Args:
        colour str: The colour the text changes to.
        text str: Content of text.
    """
    return Colours[colour].value + text + Colours.RESET.value


class GetDatetime:
    """Represent the current datetime of Dublin."""

    def __init__(self):
        """Set a time zone to Dublin."""
        self.dublin = pytz.timezone("Europe/Dublin")
        self.now = datetime.now(self.dublin)

    def now_year(self):
        """Return int: the current year."""
        return self.now.year

    def tday(self):
        """Return date: an ISO format date."""
        return self.now.date()

    def tday_str(self):
        """Return str: a DD/MM/YYYY format date."""
        return self.now.date().strftime("%d/%m/%Y")

    def now_time_str(self):
        """Return str: a HH:MM:SS format time."""
        return self.now.time().strftime("%H:%M:%S")


def convert_date(date_):
    """Split a string into a list of integers that represent
    year, month and date, and then pass them to date() object.

    Args:
        date_ str: A date - DD/MM/YYYY.
    Returns:
        date: An instance of datetime.date().
    """
    date_to_list = date_.split("/")
    int_list = list(map(int, date_to_list))
    converted_date = date(int_list[2], int_list[1], int_list[0])
    return converted_date


def convert_time(time_):
    """Split a string into a list of integers that represent
    hours, minutes and seconds if any, and then pass them to time() object.

    Args:
        time_ str: A time - %H:%M or %H:%M:%S
    return
        time: An instance of datetime.time()
    """
    time_to_list = time_.split(":")
    int_list = list(map(int, time_to_list))
    converted_time = time(int_list[0], int_list[1])
    return converted_time


def get_week(date_, result):
    """Return a list of a week(inc./excl. weekend) of the given date.

    Args:
        date_ date: An instance of datetime.date().
        result str: Including or excluding weekend.
    Returns
        list: Dates of a week starting Monday.
    """
    # Source: ALFAFA's answer on Stack Overflow
    # https://stackoverflow.com/questions/56163008
    week = date_.isocalendar()[2]
    start = date_ - timedelta(days=week)
    dates = []
    if result == "weekdays":
        for day in range(1, 6):
            dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    else:
        for day in range(1, 8):
            dates.append((start + timedelta(days=day)).strftime("%d/%m/%Y"))
    return dates


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


def display_table(table, headers=None):
    """Display a table with a solid border.

    Args:
        table list: A list of lists - The Content of the table.
                    If headers is None, all cotents display in a box.
        headers list: Names of the columns.
    """
    if headers is None:
        print(tabulate(table, tablefmt="fancy_grid"))
    else:
        print(tabulate(table, headers, tablefmt="fancy_grid"))
