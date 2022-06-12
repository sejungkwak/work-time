"""Messages module

This module provides functions that return repeated texts
throughout the application.
"""
# Custom Package
from worktime.app.utility import print_in_colour as colour


def y_or_n():
    """Return a message for a yes or no input."""
    message = f"Enter {colour('CYAN', 'y')} for yes "
    message += f"or {colour('CYAN', 'n')} for no."
    return message


def date_format():
    """Return a message for date format information."""
    message = "The date should be in the following format: "
    message += f"{colour('CYAN', 'Day/Month/Year')}."
    message += "\nFor example, 01/12/2021 is the 1st of December 2021."
    return message


def to_menu():
    """Return a message for a menu or quit option."""
    message = f"Type {colour('CYAN', 'menu')} to go back to the menu "
    message += f"or {colour('CYAN', 'quit')} to exit the system."
    return message


def invalid_year():
    """Returns an error message for invalid year absence requests."""
    message = f"\n{colour('RED', 'Unable to process your request.')}\n"
    message += f"{colour('RED', 'Absence entitlements must be')}"
    message += f"{colour('RED', 'taken within the leave year.')}"
    return message
