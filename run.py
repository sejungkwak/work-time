# External libraries
from art import *
import gspread
from google.oauth2.service_account import Credentials

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

welcome_message()
