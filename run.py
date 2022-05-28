# External libraries
from art import *
from colorama import init, Fore, Style
import gspread
from google.oauth2.service_account import Credentials

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


def welcome_message():
    """
    Display the application name and welcome message
    at the start of the system.
    """
    tprint("Work Time".center(29), font="tarty7")
    print("")
    print("Welcome to Work Time - Time Management System".center(80))
    print("")
    print("="*80)


def validate_id():
    """
    Request Employee ID and validate it against Google sheet.
    Or User can choose to contact the system administrator.
    """
    while True:
        try:
            print("\nPlease enter your employee ID.")
            print("To contact the system administrator, enter ", end="")
            print(f"{Fore.GREEN}C{Style.RESET_ALL} instead.")

            ids = [id for id, password in login_credentials]
            entered_id = input("\nEmployee ID:\n").upper()

            if entered_id == "C":
                break

            if entered_id not in ids:
                raise ValueError(
                    print(f"\nYou have entered {entered_id}.")
                )

        except ValueError:
            print("Please make sure to enter your employee ID.\n")

        else:
            break

welcome_message()
validate_id()
