# Third-party Package
from colorama import init, Fore, Style

# colorama method to enable it on Windows
init(autoreset=True)


def employee_menu():
    """Displays the menu for a logged in user as an employee."""
    numbers = range(1, 8)
    options = (["Clock In", "Clock Out", "View Clock Card",
                "View Absence Entitlements", "Book Absence",
                "Cancel Absence", "Log Out"])

    print("\nPlease choose one of the following options.\n")
    format_menu(numbers, options)


def admin_menu():
    """Displays the menu for a logged in user as an admin."""
    numbers = range(1, 5)
    options = (["Review Requests", "Review Attendance",
                "Add Employee Absence", "Log Out"])
    print("\nPlease choose one of the following options.\n")
    format_menu(numbers, options)


def format_menu(numbers, options):
    """Displays the option number in green font.

    Args:
        numbers object: A sequence of numbers.
        options list: A list of menu options.
    """
    for number, option in zip(numbers, options):
        print(f"{Fore.GREEN}{number}{Style.RESET_ALL} {option}")
