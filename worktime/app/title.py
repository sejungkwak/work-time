# Third-party Package
from art import *

# Custom Package
from worktime.app import utility
from worktime.worksheets.employees import Employees


def title_main():
    """Display the application name at the start of the system."""
    utility.clear()
    tprint("Work Time".center(29), font="tarty7")
    print("\n" + "Time Management System".center(80))
    print("\n" + "="*80 + "\n")


def title_employee(id):
    """Display the title and welcome message for the employee portal.

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    fname = Employees(id).get_fname()
    tprint("Employee Portal".center(18), font="rectangles")
    print(f"Welcome back, {fname}!".center(80))
    print("\n" + "="*80)


def title_admin():
    """Display the title and welcome message for the admin portal."""
    utility.clear()
    tprint("Admin Portal".center(24), font="rectangles")
    print("Welcome back!".center(80))
    print("\n" + "="*80)


def title_end():
    """Display an end of the system title."""
    utility.clear()
    print("\n"*5)
    tprint("Thank You!".center(25), font="rectangles")
