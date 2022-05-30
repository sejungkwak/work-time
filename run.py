# Built-in Modules
from os import name, system
import time

# Third-party libraries
from art import *
from colorama import init, Fore, Style
import gspread
from google.oauth2.service_account import Credentials
from passlib.hash import pbkdf2_sha256
import stdiomask

# colorama method to enable it on Windows
init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("work_time")

cred_sheet = SHEET.worksheet("login_credentials")
login_credentials = cred_sheet.get_all_values()


# Source: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    """
    Clear the screen.
    """
    system("cls" if name == "nt" else "clear")


def welcome_message():
    """
    Display the application name and welcome message
    at the start of the system.
    """
    tprint("Work Time".center(29), font="tarty7")
    print("\n" + "Welcome to Work Time - Time Management System".center(80))
    print("\n" + "="*80 + "\n")


def validate_id():
    """
    Request Employee ID and validate it against Google sheet.
    Or User can choose to contact the system administrator.

    Raises:
        ValueError: If the input employee id is incorrect.
    """
    while True:
        try:
            print("Please enter your employee ID.")
            print("To contact the system administrator, enter ", end="")
            print(f"{Fore.GREEN}HELP{Style.RESET_ALL} instead.")

            ids = [id for id, password in login_credentials]
            entered_id = input("\nEmployee ID:\n").upper()

            if entered_id == "HELP":
                break

            if entered_id not in ids:
                raise ValueError(
                    print("You have entered an invalid ID.")
                )

        except ValueError:
            print("Please make sure to enter your employee ID.\n")

        else:
            return validate_pw(entered_id)
            break


def validate_pw(id):
    """
    Run when the user input a valid employee ID.
    Request Password and validate it against Google sheet.

    Args:
        :id str: Employee Id that was used to log in.

    Raises:
        ValueError: If the input password is incorrect.
    """
    password_col = 2
    id_index = cred_sheet.find(id).row
    password = cred_sheet.cell(id_index, password_col).value

    while True:
        try:
            entered_password = stdiomask.getpass(prompt="\nPassword:\n")
            verify = pbkdf2_sha256.verify(entered_password, password)

            if not verify:
                raise ValueError(
                    print("You have entered an incorrect password.")
                )

        except ValueError:
            print("Please try again.")

        else:
            if id == "ADMIN":
                pass
            else:
                run_employee_portal(id)
                employee_menu(id)
            break


def get_datetime():
    """
    Return the current date and time in dictionary.
    """
    local_time = time.localtime()
    get_date = time.strftime("%d/%m/%Y", local_time)
    get_time = time.strftime("%H:%M:%S", local_time)
    return {"date": get_date, "time": get_time}


def get_name(id):
    """
    Return the employee's first name from the worksheet.

    Args:
        :id str: Employee Id that was used to log in.
    """
    employees_sheet = SHEET.worksheet("employees")
    fname_col = 2
    id_index = employees_sheet.find(id).row
    fname = employees_sheet.cell(id_index, fname_col).value
    return fname


def run_employee_portal(id):
    """
    Display the title and welcome message for the employee portal.

    Args:
        :id str: Employee Id that was used to log in.
    """
    name = get_name(id)
    clear()
    tprint("Employee Portal".center(18), font="smshadow")
    print("\n" + f"Welcome back, {name}!".center(80))
    print("\n" + "="*80)


def employee_menu(id):
    """
    Display the employee portal menu.
    """
    print("\nPlease choose one of the following options.\n")
    print(f"{Fore.GREEN}1{Style.RESET_ALL} Clock In")
    print(f"{Fore.GREEN}2{Style.RESET_ALL} Clock Out")
    print(f"{Fore.GREEN}3{Style.RESET_ALL} View Clock Card")
    print(f"{Fore.GREEN}4{Style.RESET_ALL} View Absence Entitlements")
    print(f"{Fore.GREEN}5{Style.RESET_ALL} Book Absence")
    print(f"{Fore.GREEN}6{Style.RESET_ALL} Cancel Absence")
    print(f"{Fore.GREEN}7{Style.RESET_ALL} Log Out")
    choice = validate_menu_choice()
    if choice == "1":
        return clock_in(id)
    elif choice == "2":
        return clock_out(id)
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        pass
    else:
        pass


def validate_menu_choice():
    """
    Return the user choice from the employee portal menu.

    Args:
        :id str: Employee Id that was used to log in.

    Raises:
        ValueError: If the input type is not a digit,
                    or the input value is out of range.
    """
    while True:
        try:
            choice = input("\nPlease enter a number to continue:\n")

            if not choice.isdigit():
                raise ValueError(
                    print("Please enter a number.")
                )
            elif int(choice) not in range(1, 8):
                raise ValueError(
                    print("Please enter a number between 1 and 7.")
                )

        except ValueError:
            print("Please try again.")

        else:
            return choice
            break


def clock_in(id):
    """
    Run when the user chooses clock in option.
    Send the clock in data to the worksheet.

    Args:
        :id str: Employee Id that was used to log in.
    """
    now = get_datetime()
    today = now["date"]
    clock_in_at = now["time"]

    clock_sheet = SHEET.worksheet("clockings")
    clockings = clock_sheet.get_all_values()

    option = (f"Enter {Fore.GREEN}Y {Style.RESET_ALL}to overwrite "
              f"or {Fore.GREEN}N {Style.RESET_ALL}to go back to menu.")

    for clocking in clockings:
        user_id, date, clocked_in, clocked_out = clocking

        if id == user_id and today == date and clocked_in:
            is_overwrite = check_for_clockin_overwrite(clocked_in, option)
            if is_overwrite == "Y":
                row_index = clock_sheet.find(id).row
                clock_in_col = 3
                clock_sheet.update_cell(row_index, clock_in_col, clock_in_at)
                print(f"Clock in time has been updated: {clock_in_at}")
                break
            else:
                break
    else:
        data = [id, today, clock_in_at]
        update_sheet = clock_sheet.append_row(data)
        clear()
        print(f"You have successfully clocked in at {clock_in_at}.")

    print("Going back to the menu...")
    time.sleep(2)
    clear()
    employee_menu(id)


def check_for_clockin_overwrite(clocked_in, message):
    """
    Return the user answer.

    Args:
        :message str: Options that displays when the user answer is invalid.
    """
    print(f"You have already clocked in for today at {clocked_in}.")
    print(f"Would you like to overwrite it?")
    print(message)
    while True:
        try:
            answer = input("Please enter your answer here:\n").upper()
            answers = ["Y", "N"]
            if answer not in answers:
                raise ValueError(
                    print(f"Your answer is invalid: {answer}.")
                )
        except ValueError:
            print(message)
        else:
            return answer


def clock_out(id):
    """
    Run when the user chooses clock out option.
    Send the clock out data to the worksheet.

    Args:
        :id str: Employee Id that was used to log in.
    """
    now = get_datetime()
    today = now["date"]
    clock_out_at = now["time"]

    clock_sheet = SHEET.worksheet("clockings")
    clockings = clock_sheet.get_all_values()

    for clocking in clockings:
        user_id, date, clocked_in, clocked_out = clocking
        if id == user_id and today == date:
            if clocked_out:
                print(f"{Fore.RED}You have already ",
                      f"{Fore.RED}clocked out at {clocked_out}.")
                print("Please contact your manager ",
                      "to update your clock out time.")
                break
            else:
                row_index = clock_sheet.find(id).row
                clock_out_col = 4
                clock_sheet.update_cell(row_index, clock_out_col, clock_out_at)
                print(f"You have successfully clocked out at {clock_out_at}.")
                break
    else:
        data = [id, today, "", clock_out_at]
        clock_sheet.append_row(data)
        print(f"{Fore.RED}You did not clock in today.")
        print("Please contact your manager to add your clock in time.")
        print(f"You have successfully clocked out at {clock_out_at}.")

    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)

welcome_message()
validate_id()
