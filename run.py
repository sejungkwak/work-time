"""Work Time Initial Module

This module handles the login process.
"""

# Built-in Modules
from itertools import groupby
import sys

# Third-party Packages
import stdiomask

# Custom Packages
from worktime.app import admin, employee, title, utility, validations
from worktime.app.utility import print_in_colour as colour
from worktime.worksheets import credentials, entitlements, requests


def login():
    """Request Employee ID and password. Validate the user input.
    Run a while loop until the user enters a valid ID and password.
    """
    help_typed = False
    all_creds = credentials.Credentials().credentials
    all_ids = [id for id, pw in all_creds]

    while True:
        print("\nPlease enter " + colour("CYAN", "Employee ID") + ".")
        if not help_typed:
            print("For more information about Work Time,",
                  f"type {colour('CYAN', 'help')} and press enter.")
        id_ = input(colour("CYAN", ">>>\n")).upper().strip()

        if id_ == "HELP":
            help_()
            print("\nPlease enter " + colour("CYAN", "Employee ID") + ".")
            id_ = input(colour("CYAN", ">>>\n")).upper().strip()
            help_typed = True

        print(f"\nPlease enter {colour('CYAN', 'Password')}.")
        pw_ = stdiomask.getpass(prompt=colour("CYAN", ">>>\n"))
        correct_pw = get_pw(id_, all_creds)

        if validations.validate_login(id_, pw_, all_ids, correct_pw):
            if id_ == "ADMIN":
                title.display_admin_title()
                admin.ReviewRequests()
                admin.admin_main()
                break
            title.display_employee_title(id_)
            employee.employee_main(id_)
            break


def get_pw(id_, data):
    """Returns a matching password for the ID.

    Args:
        id_ str: An employee ID.
        data list: A list containing employee ID and password.
    Returns:
        str: The matching password for the ID.
    """
    for credential in data:
        if id_ in credential:
            index = data.index(credential)
            password = data[index][1]
            return password


def help_():
    """Print application information."""
    text = f"""
{colour('CYAN', 'About the application')}
Work Time is an employee time management system. It provides
an employee clocking system, attendance tracking and absence
management.

{colour('CYAN', 'Employee Portal')}
It offers the following 6 options to choose from: Clock In,
Clock Out, View Clock Card, View Absence Entitlements, Book
Absence, Cancel Absence.

{colour('CYAN', 'Admin Portal')}
It offers the following 4 options to choose from: Review
Requests, Review Attendance, Add absence, Update Clock Card.

{colour('CYAN', 'Contact the developer')}
If you would like to report a bug, suggest an idea or require
additional help, please email me at kwak.sejung@gmail.com
"""
    utility.display_table([[text]])


def calc_req_hours():
    """Calculate absence request hours from absence_requests worksheet.
    This function is for updating taken hours.
    """
    all_req = requests.Requests().requests
    all_req.sort(key=lambda req: req[1])
    groups = groupby(all_req, lambda req: req[1])
    new_list = [[item for item in data] for (key, data) in groups]
    entitle_list = []
    for each_employee in new_list:
        taken = 0
        planned = 0
        pending = 0
        for each_req in each_employee:
            start_date = utility.convert_date(each_req[2])
            tday = utility.GetDatetime().tday()
            if ((start_date - tday).days <= 0 and
                    each_req[-2] == "True" and
                    each_req[-1] == "False"):
                taken += int(float(each_req[-4]) * 8)
            elif ((start_date - tday).days > 0 and
                    each_req[-2] == "True" and
                    each_req[-1] == "False"):
                planned += int(float(each_req[-4]) * 8)
            elif ((start_date - tday).days > 0 and
                    each_req[-2] != "False" and
                    each_req[-1] == "False"):
                pending += int(float(each_req[-4]) * 8)
            unallocated = 200 - (taken + planned + pending)
            each_entitle = [each_req[1], 200, taken,
                            planned, pending, unallocated]
        entitle_list.append(each_entitle)
    return entitle_list


def update_entitlements():
    """Update entitlements hours to entitlements worksheet."""
    ent_class = entitlements.Entitlements()
    ents = ent_class.entitlements
    updated_ents = calc_req_hours()
    if ents == updated_ents:
        return
    for ent in ents:
        for updated_ent in updated_ents:
            if ent[0] == updated_ent[0]:
                ents[ents.index(ent)] = updated_ent
    ent_class.worksheet.update("A2:F11", ents)


def main():
    """In the try block, call functions to update entitlement hours,
    display the title and a login prompt.
    In the except block, catch KeyboardInterrupt which is caused by a user
    pressing Ctrl + C, and exit the application.
    """
    try:
        update_entitlements()
        title.display_main_title()
        login()
    except KeyboardInterrupt:
        title.display_goodbye()
        sys.exit()


if __name__ == "__main__":
    main()
