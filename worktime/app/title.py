# Built-in Modules
import time

# Custom Package
from worktime.app import utility
from worktime.worksheets.employees import Employees

portal = """
                ██████   ██████  ██████  ████████  █████  ██
                ██   ██ ██    ██ ██   ██    ██    ██   ██ ██
                ██████  ██    ██ ██████     ██    ███████ ██
                ██      ██    ██ ██   ██    ██    ██   ██ ██
                ██       ██████  ██   ██    ██    ██   ██ ███████
"""


def title_main():
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
    print("\n" + "="*80 + "\n")


def title_employee(id):
    """Display the title and welcome message for the employee portal.

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    fname = Employees(id).get_fname()
    print("""
      ███████ ███    ███ ██████  ██       ██████  ██    ██ ███████ ███████
      ██      ████  ████ ██   ██ ██      ██    ██  ██  ██  ██      ██
      █████   ██ ████ ██ ██████  ██      ██    ██   ████   █████   █████
      ██      ██  ██  ██ ██      ██      ██    ██    ██    ██      ██
      ███████ ██      ██ ██      ███████  ██████     ██    ███████ ███████
    """)
    print(portal)
    print(f"Welcome back, {fname}!".center(80))
    print("\n" + "="*80)
    time.sleep(3)
    utility.clear()


def title_admin():
    """Display the title and welcome message for the admin portal."""
    utility.clear()
    print("""
                     █████  ██████  ███    ███ ██ ███    ██
                    ██   ██ ██   ██ ████  ████ ██ ████   ██
                    ███████ ██   ██ ██ ████ ██ ██ ██ ██  ██
                    ██   ██ ██   ██ ██  ██  ██ ██ ██  ██ ██
                    ██   ██ ██████  ██      ██ ██ ██   ████
    """)
    print(portal)
    print("Welcome back!".center(80))
    print("\n" + "="*80)
    time.sleep(3)
    utility.clear()


def title_help():
    """Display the title for the help portal."""
    utility.clear()
    print("""

                        ██   ██ ███████ ██      ██████
                        ██   ██ ██      ██      ██   ██
                        ███████ █████   ██      ██████
                        ██   ██ ██      ██      ██
                        ██   ██ ███████ ███████ ██

    """)
    print(portal)
    print("\n" + "="*80)
    time.sleep(3)
    utility.clear()


def title_end():
    """Display an end of the system title."""
    utility.clear()
    print("\n"*8)
    print("""
        ██████   ██████   ██████  ██████      ██████  ██    ██ ███████ ██
       ██       ██    ██ ██    ██ ██   ██     ██   ██  ██  ██  ██      ██
       ██   ███ ██    ██ ██    ██ ██   ██     ██████    ████   █████   ██
       ██    ██ ██    ██ ██    ██ ██   ██     ██   ██    ██    ██
        ██████   ██████   ██████  ██████      ██████     ██    ███████ ██
    """)
