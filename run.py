# Built-in Modules
from os import name, system
from time import sleep

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
    """
    password_column = 2
    id_index = cred_sheet.find(id).row
    password = cred_sheet.cell(id_index, password_column).value

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
                employee_menu(id)
            break


def get_name(id):
    """
    Get the employee's first name from the worksheet.
    """
    employees_sheet = SHEET.worksheet("employees")
    fname_column = 2
    id_index = employees_sheet.find(id).row
    fname = employees_sheet.cell(id_index, fname_column).value
    return fname


def employee_menu(id):
    """
    Create menu for employee.
    """
    name = get_name(id)
    clear()
    tprint("Employee Portal".center(25), font="tarty3")
    print("\n" + f"Welcome back, {name}!".center(80))
    print("\n" + "="*80)

    while True:
        try:
            print("\nPlease choose one of the following options.\n")
            print(f"{Fore.GREEN}1{Style.RESET_ALL} Clock In")
            print(f"{Fore.GREEN}2{Style.RESET_ALL} Clock Out")
            print(f"{Fore.GREEN}3{Style.RESET_ALL} View Clock Card")
            print(f"{Fore.GREEN}4{Style.RESET_ALL} View Absence Entitlements")
            print(f"{Fore.GREEN}5{Style.RESET_ALL} Book Absence")
            print(f"{Fore.GREEN}6{Style.RESET_ALL} Cancel Absence")
            choice = input("\nPlease enter a number to continue:\n")

            if not choice.isdigit():
                raise ValueError(
                    print("Please enter a number.")
                )
            elif int(choice) not in range(1, 7):
                raise ValueError(
                    print("Please enter a number between 1 and 6.")
                )

        except ValueError:
            print("Please try again.")
            sleep(3)
            clear()

        else:
            if choice == "1":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                pass
            elif choice == "5":
                pass
            elif choice == "6":
                pass
            break

welcome_message()
validate_id()
