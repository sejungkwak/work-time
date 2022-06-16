"""Title Module

This module displays title arts for the application main, employee portal,
admin portal and exit screen.
"""

# Custom Packages
from worktime.app import utility
from worktime.worksheets.employees import Employees

PORTAL = """
                ██████   ██████  ██████  ████████  █████  ██
                ██   ██ ██    ██ ██   ██    ██    ██   ██ ██
                ██████  ██    ██ ██████     ██    ███████ ██
                ██      ██    ██ ██   ██    ██    ██   ██ ██
                ██       ██████  ██   ██    ██    ██   ██ ███████
"""


def display_main_title():
    """Display the application name at the start of the system."""
    utility.clear()
    print("""
 ██████████████████████████████████████████████████████████████████████████████
 ███  █████  ██      ██      ██  ███  █████        █  █   ████   █       ██████
 ███  █████  █  ████  █  ███  █  ██  █████████  ████  █    ██    █  ███████████
 ███  ██ ██  █  ████  █      ██     ██████████  ████  █  █    █  █     ████████
 ███  █   █  █  ████  █  ███  █  ██  █████████  ████  █  ██  ██  █  ███████████
 ▀▀▀▀▄▄▄▀▄▄▄▀▀▀▄▄▄▄▄▄▀▀▄▄▀▀▀▄▄▀▄▄▀▀▀▄▄▀▀▀▀▀▀▀▀▄▄▀▀▀▀▄▄▀▄▄▀▀▀▀▀▀▄▄▀▄▄▄▄▄▄▄▀▀▀▀▀▀
    """)
    print("\n" + "Time Management System".center(80))
    print("\n" + "=" * 80)


def display_employee_title(id_):
    """Display the title and welcome message for the employee portal.

    Args:
        id_ str: Employee ID that was used to log in.
    """
    utility.clear()
    fname = Employees(id_).get_fname()
    print("""
      ███████ ███    ███ ██████  ██       ██████  ██    ██ ███████ ███████
      ██      ████  ████ ██   ██ ██      ██    ██  ██  ██  ██      ██
      █████   ██ ████ ██ ██████  ██      ██    ██   ████   █████   █████
      ██      ██  ██  ██ ██      ██      ██    ██    ██    ██      ██
      ███████ ██      ██ ██      ███████  ██████     ██    ███████ ███████
    """)
    print(PORTAL)
    print(f"Welcome back, {fname}!".center(80))
    print("\n")


def display_admin_title():
    """Display the title and welcome message for the admin portal."""
    utility.clear()
    print("""
                     █████  ██████  ███    ███ ██ ███    ██
                    ██   ██ ██   ██ ████  ████ ██ ████   ██
                    ███████ ██   ██ ██ ████ ██ ██ ██ ██  ██
                    ██   ██ ██   ██ ██  ██  ██ ██ ██  ██ ██
                    ██   ██ ██████  ██      ██ ██ ██   ████
    """)
    print(PORTAL)
    print("Welcome back!".center(80))
    print("\n")


def display_goodbye():
    """Display an end of the system title."""
    utility.clear()
    print("\n" * 12)
    print("""
        ██████   ██████   ██████  ██████  ██████  ██    ██ ███████ ██
       ██       ██    ██ ██    ██ ██   ██ ██   ██  ██  ██  ██      ██
       ██   ███ ██    ██ ██    ██ ██   ██ ██████    ████   █████   ██
       ██    ██ ██    ██ ██    ██ ██   ██ ██   ██    ██    ██
        ██████   ██████   ██████  ██████  ██████     ██    ███████ ██
    """)
