"""Menu Module

This module provides functions that display numbered menu options in a box.
"""

# Custom Package
from worktime.app import utility
from worktime.app.utility import print_in_colour as colour


def employee_menu():
    """Displays the menu for a logged-in user as an employee."""
    numbers = range(1, 8)
    options = (["Clock In", "Clock Out", "View Clock Card",
                "View Absence Entitlements", "Book Absence",
                "Cancel Absence", "Exit"])
    format_menu(numbers, options)


def admin_menu():
    """Displays the menu for a logged-in user as an admin."""
    numbers = range(1, 6)
    options = (["Review Requests", "Review Attendance",
                "Add Absence", "Update Clock Card", "Exit"])
    format_menu(numbers, options)


def absence_period_menu():
    """Displays the menu for absence period."""
    numbers = range(1, 5)
    options = (["9:30AM-1:30PM", "1:30PM-5:30PM",
                "Full day", "More than 2 consecutive days"])
    format_menu(numbers, options)


def absence_paid_menu():
    """Displays the menu for absence paid type."""
    numbers = range(1, 3)
    options = ["Paid Absence(Taken from entitlements)", "Unpaid Absence"]
    format_menu(numbers, options)


def update_clocking_menu():
    """Displays the menu for update clock cards."""
    numbers = range(1, 3)
    options = ["Update clock in time", "Update clock out time"]
    format_menu(numbers, options)


def format_menu(numbers, options):
    """Displays the option number in cyan font.

    Args:
        numbers object: A sequence of numbers.
        options list: A list of menu options.
    """
    items = f"Enter a {colour('CYAN', 'number')} to select "
    items += "one of the following options.\n\n"
    for number, option in zip(numbers, options):
        items += f"{colour('CYAN', str(number))}  {option}\n"
    table = [[items]]
    utility.display_table(table)
