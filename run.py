# Built-in Modules
import sys

# Third-party Packages
import stdiomask

# Custom Packages
from worktime.app import admin, employee, tables, title, utility, validations
from worktime.worksheets import credentials


def get_employee_id():
    """Request Employee ID and validate the user input.
    Run a while loop until the user types "help" or a valid ID.
    """
    ids = credentials.Credentials().ids()
    infor_printed = False

    while True:
        print(f"Please enter {utility.cyan('Employee ID.')}")
        if not infor_printed:
            print("For more information about Work Time,",
                  f"type {utility.cyan('help')} and press enter.")
        entered_id = input(f"{utility.cyan('>>>')}\n").upper().strip()
        utility.clear()

        if entered_id == "HELP":
            help_()
            infor_printed = True
        elif validations.validate_id(entered_id, ids):
            get_pw(entered_id)
            break


def get_pw(id):
    """Request password and validate the user input.
    Run a while loop until the user types "help" or a correct password.

    Args:
        id str: Employee ID that was entered to log in.
    """
    pw = credentials.Credentials().pw(id)
    while True:
        print(f"Please enter {utility.cyan('Password')}.")
        password = stdiomask.getpass(prompt=f"{utility.cyan('>>>')}\n")
        utility.clear()

        if validations.validate_pw(password, pw):
            if id == "ADMIN":
                title.title_admin()
                admin.admin_main()
                break
            else:
                title.title_employee(id)
                employee.employee_main(id)
                break


def help_():
    """Print application information."""
    text = f"""
{utility.cyan('About the application')}
Work Time is an employee time management system. It provides an employee
clocking system, attendance tracking and absence management.

{utility.cyan('Employee Portal')}
It offers the following 6 options to choose from: Clock In, Clock Out, View
Clock Card, View Absence Entitlements, Book Absence, Cancel Absence.

{utility.cyan('Admin Portal')}
It offers the following 4 options to choose from: Review Requests, Review
Attendance, Add absence, Update Clock Card.

{utility.cyan('Contact the developer')}
If you would like to report a bug, suggest an idea or require additional help,
please email me at kwak.sejung@gmail.com
"""
    tables.display_table([[text]])


if __name__ == "__main__":
    try:
        title.title_main()
        get_employee_id()
    except KeyboardInterrupt:
        title.title_end()
        sys.exit()
