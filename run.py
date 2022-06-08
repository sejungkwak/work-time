# Built-in Modules
import sys

# Third-party Packages
import stdiomask

# Custom Packages
from worktime.app import admin, employee, title, utility, validations


def get_employee_id():
    """Request Employee ID and validate the user input.
    Run a while loop until the user types "help" or a valid ID.
    """
    while True:
        print("Please enter your Employee ID.")
        print("To contact the system administrator, enter",
              f"{utility.cyan('help')} instead.")
        entered_id = input("\nEmployee ID:\n").upper().strip()

        if entered_id == "HELP":
            break

        if validations.validate_id(entered_id):
            get_pw(entered_id)
            break


def get_pw(id):
    """Request password and validate the user input.
    Run a while loop until the user types "help" or a correct password.

    Args:
        id str: Employee ID that was entered to log in.
    """
    while True:
        password = stdiomask.getpass(prompt="\nPassword:\n")
        if password.upper() == "HELP":
            break

        is_valid = validations.validate_pw(id, password)
        if is_valid:
            if id == "ADMIN":
                title.title_admin()
                admin.new_request_notification()
                admin.admin_main()
                break
            else:
                title.title_employee(id)
                employee.employee_main(id)
                break


if __name__ == "__main__":
    try:
        title.title_main()
        get_employee_id()
    except KeyboardInterrupt:
        title.title_end()
        sys.exit()
