"""Validations Module

This module provides functions that validate a user input.
"""

# Built-in Modules
from datetime import datetime

# Third-party Packages
from passlib.hash import pbkdf2_sha256

# Custom Packages
from worktime.app import utility
from worktime.app.utility import print_in_colour as colour


def validate_login(id_, pw_, all_ids, correct_pw):
    """In the try block, compare the given ID and password
    to the list of IDs and matching password.

    Args:
        id_ str: User input value for employee ID.
        pw_ str: User input value for password.
        all_ids: All employees' IDs.
        correct_pw: The matching password.
    Returns:
        bool: True if the ID in the list, False otherwise.
    Raises:
        ValueError: If the ID is not in the ID list
                    or the password does not match.
        TypeError: If the input value is None.
    """
    try:
        valid_pw = pbkdf2_sha256.verify(pw_, correct_pw)
        if id_ not in all_ids:
            raise ValueError()
        if not valid_pw:
            raise ValueError()
    except ValueError:
        print(colour("RED", "Invalid employee ID or password."))
        return False
    except TypeError:
        print(colour("RED", "Invalid employee ID or password."))
        return False
    else:
        return True


def validate_id(id_, ids):
    """In the try block, compare the given ID to the list of IDs.

    Args:
        id_ str: User input value.
        ids list: Employee IDs with matching password.
    Returns:
        bool: True if the ID in the list, False otherwise.
    Raises:
        ValueError: If the ID is not in the ID list.
    """
    try:
        if id_ not in ids:
            raise ValueError()
    except ValueError:
        print(colour("RED", "Invalid employee ID: " + id_))
        return False
    else:
        return True


def validate_choice_number(choice, numbers):
    """In the try block, convert a string value into an integer.

    Args:
        choice str: User input value.
        numbers list: Numbered options.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ValueError: If the input value is not a digit or out of range.
    """
    try:
        choice = int(choice)
        if choice not in numbers:
            raise ValueError()
    except ValueError:
        print(colour("RED", "Invalid value: " + str(choice)) + "\n")
        return False
    else:
        return True


def validate_choice_letter(choice, choices):
    """In the try block, check if the user entered a valid input.

    Args:
        choice str: User input value.
        choices list: A list of options the user needs to choose from.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ValueError: If the input value is not in the list.
    """
    try:
        if choice not in choices:
            raise ValueError()
    except ValueError:
        print(colour("RED", "Invalid value: " + choice))
        return False
    else:
        return True


def validate_date(date_):
    """In the try block, compare user input to the date format.

    Args:
        date_ str: A value the user has entered for the date.
    Returns:
        date: A ISO format date if successful.
        bool: False if exceptions raised.
    Raises:
        ValueError: If the date is invalid or "/" is not used to separate
                    the year, month and date.
    """
    try:
        date_format = "%d/%m/%Y"
        new_date = datetime.strptime(date_, date_format).date()
    except ValueError:
        print(colour("RED", "Invalid value: " + date_))
        return False
    else:
        return new_date


def validate_time(time_):
    """In the try block, compare user input to the time format.

    Args:
        time_ str: A value the user has entered for the time.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ValueError: If the time is invalid or ":" is not used to separate
                    the hours and minutes.
    """
    try:
        time_format = "%H:%M"
        datetime.strptime(time_, time_format).time()
    except ValueError:
        print(colour("RED", "Invalid value: " + time_))
        return False
    else:
        return True


def validate_days(date1, date2, unallocated):
    """In the try block, calculate total number of weekdays between 2 given dates.

    Args:
        date1 str: The start date.
        date2 str: The end date.
        unallocated str: Total available absence hours.
    Returns:
        int: Total number of weekdays between date1 and date2.
        bool: False if exceptions raised.
    Raises:
        ValueError: If request hours are exceeding the unallocated hours
                    or the end date is before start date.
    """
    try:
        num_of_days = utility.get_num_of_weekdays(date1, date2)
        num_of_hours = num_of_days * 8
        if num_of_hours > int(unallocated):
            raise ValueError(
                print(colour("RED", "Insufficient paid time off available."))
            )
        if num_of_days < 2:
            raise ValueError(
                print(colour("RED", "Absence end date must be " +
                      "after absence start date."))
            )
    except ValueError:
        return False
    else:
        return num_of_days


def validate_unpaid_days(date1, date2):
    """In the try block, calculate total number of weekdays.

    Args:
        date1 str: The start date.
        date2 str: The end date.
    Returns:
        int: Total number of weekdays between date1 and date2.
        bool: False if exceptions raised.
    Raises:
        ValueError: If the absence end date is before start date.
    """
    try:
        num_of_days = utility.get_num_of_weekdays(date1, date2)
        if num_of_days < 2:
            raise ValueError(
                print(colour("RED", "Absence end date must be " +
                      "after absence start date.\n"))
            )
    except ValueError:
        return False
    else:
        return num_of_days
