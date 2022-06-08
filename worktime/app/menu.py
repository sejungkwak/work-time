# Custom Package
from worktime.app import utility


def employee_menu():
    """Displays the menu for a logged in user as an employee."""
    numbers = range(1, 8)
    options = (["Clock In", "Clock Out", "View Clock Card",
                "View Absence Entitlements", "Book Absence",
                "Cancel Absence", "Log Out"])
    format_menu(numbers, options)


def admin_menu():
    """Displays the menu for a logged in user as an admin."""
    numbers = range(1, 5)
    options = (["Review Requests", "Review Attendance",
                "Add Employee Absence", "Log Out"])
    format_menu(numbers, options)


def absence_menu():
    """Displays the menu for absence."""
    numbers = range(1, 5)
    options = (["9:30AM-1:30PM", "1:30PM-5:30PM",
                "Full day", "More than 2 consecutive days"])
    format_menu(numbers, options)


def format_menu(numbers, options):
    """Displays the option number in green font.

    Args:
        numbers object: A sequence of numbers.
        options list: A list of menu options.
    """
    print("\nPlease choose one of the following options.\n")
    for number, option in zip(numbers, options):
        print(f" {utility.green(str(number))} {option}")
