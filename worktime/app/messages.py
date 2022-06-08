# Custom Package
from worktime.app import utility


def y_or_n():
    """Return a message for a yes or no input."""
    message = f"Enter {utility.cyan('y')} for yes "
    message += f"or {utility.cyan('n')} for no:"
    return message


def enter_number():
    """Return a message for a digit input."""
    return "Enter a number here:"


def enter_date():
    """Return a message for a date input."""
    return "Enter a date here:"


def enter_menu():
    """Return a message for menu or quit input."""
    return "Type menu or quit here:"


def enter_req_id():
    """Return a message for an absence request ID input."""
    return "Enter a request ID here:"


def enter_ee_id():
    """Return a message for a employee ID input."""
    return "Enter an employee ID here:"


def date_format():
    """Return a message for date format information."""
    message = "The date should be in the following format: "
    message += f"{utility.cyan('Day/Month/Year')}."
    message += "\nFor example, 01/12/2021 is the 1st of December 2021."
    return message


def to_menu():
    """Return a message for a menu or quit option."""
    message = f"Type {utility.cyan('menu')} to go back to the menu "
    message += f"or {utility.cyan('quit')} to exit the system."
    return message


def invalid_year():
    """Returns an error message for invalid year absence requests."""
    message = f"\n{utility.red('Unable to process your request.')}\n"
    message += f"{utility.red('Absence entitlements must be')}"
    message += f"{utility.red('taken within the leave year.')}"
    return message
