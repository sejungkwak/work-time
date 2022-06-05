# Built-in Modules
import sys

# Third-party Packages
from colorama import init, Fore, Style

# Custom Package
from worktime.app import menu, tables, title, utility, validations
from worktime.worksheets import clockings, employees, entitlements, requests

# colorama method to enable it on Windows
init(autoreset=True)


def admin_main():
    """Request a number between 1 and 4, the numbered options.
    Run a while loop until the user inputs a valid number.
    """
    title.title_admin()
    requests_notification_message()
    while True:
        menu.admin_menu()
        choice = input("\nPlease enter a number to continue:\n").strip()
        if validations.validate_choice_number(choice, range(1, 5)):
            break

    if choice == "1":
        display_requests()
    elif choice == "2":
        display_attendance()
    elif choice == "3":
        add_absence()
    else:
        title.title_end()
        sys.exit()


def requests_notification_message():
    """Check if there are new requests and display the result."""
    new_requests = requests.Requests().get_new_requests()
    if len(new_requests) > 0:
        print(f"\n{Fore.GREEN}You have",
              f"{Fore.GREEN}{len(new_requests)} request(s) to review.")
    else:
        print("\nThere are no more requests to review right now.")


def display_requests():
    """Display new requests and ask the user to choose a number."""
    requests_notification_message()
    new_requests = requests.Requests().get_new_requests()
    if len(new_requests) > 0:
        print("Getting data...")
        tables.display_new_requests()
        while True:
            id_list = [int(list[0]) for list in new_requests]
            print("\nEnter the request ID in the first column",
                  "you want to approve or reject.")
            choice = input("Please enter your answer here:\n").strip()
            if validations.validate_choice_number(choice, id_list):
                break

        action = get_action_type()

        print("Processing...")
        requests_row_index = int(choice) + 1
        requests.Requests().update_approved(requests_row_index, action)

        employee_id = get_employee_id(choice)
        absence_days = requests.Requests().get_duration(requests_row_index)
        hours = int(float(absence_days) * 8)
        entitlements_sheet = entitlements.Entitlements(employee_id)
        entitlements_sheet.update_hours("pending", hours, "subtract")
        if action == "APPROVE":
            entitlements_sheet.update_hours("planned", hours, "add")
        else:
            entitlements_sheet.update_hours("unallocated", hours, "add")
        print("Data has been updated successfully.")
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        admin_main()
    else:
        title.title_end()
        sys.exit()


def get_action_type():
    """Run a while loop until the user types "approve" or "reject".

    Returns:
        str: User input value.
    """
    while True:
        print(f"\nEnter {Fore.GREEN}approve",
              "to approve the request",
              f"or {Fore.GREEN}reject {Style.RESET_ALL}to reject.")
        choice = input("Please enter your answer here:\n").upper().strip()
        if validations.validate_choice_letter(choice, ["APPROVE", "REJECT"]):
            return choice


def get_employee_id(request_id):
    """Check the corresponding employee ID to the request ID.

    Args:
        :request_id str: Request ID on the requests worksheet.

    Returns:
        str: An employee ID.
    """
    new_requests = requests.Requests().requests
    for request in new_requests:
        if request_id == request[0]:
            employee_id = request[1]
            return employee_id


def display_attendance():
    """Display the current week's clock cards and then ask if they want to
    review other weeks. Run a while loop until they input a valid answer.
    """
    print("Getting this week's clock cards data...")
    if get_clock_cards():
        print("Clock cards display from Monday to Sunday.")

    while True:
        print("\nIf you would like to review other weeks,",
              "please enter the date that you want to review.")
        print("The date should be in the following format:",
              f"{Fore.GREEN}Day/Month/Year")
        print(f"For example, {Fore.GREEN}01/12/2021",
              "for the 1st of December 2021.")
        print(f"To go back to the menu, type {Fore.GREEN}menu",
              f"and to quite the system, type {Fore.GREEN}quit.")
        answer = input("Please enter the date here:\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        else:
            if validations.validate_date(answer):
                get_clock_cards(answer)


def get_clock_cards(date=None):
    """Check if there is any clock in/out data for the week of
    the passed date and display it.

    Args:
        :date str: A DD/MM/YYYY formatted date.

    Retruns:
        bool: True if there are clock cards, False otherwise.
    """
    today = utility.get_current_datetime()["date"]
    date = today if date is None else date

    all_ees = employees.Employees()
    ee_ids = [ee[0] for ee in all_ees.employees]
    data = False
    for ee_id in ee_ids:
        clock_sheet = clockings.Clockings(ee_id)
        if clock_sheet.get_week_clockings(date):
            tables.display_clock_card(ee_id, date)
            data = True
        else:
            print(f"No data found for {ee_id}.")
    return data


def add_absence():
    """Get an employee ID, duration, start date and end date from the user
    and update data to worksheet.
    """
    ee_id = get_ee_id()
    pto_hours = check_pto_hours()
    absence_type = get_absence_type()
    if absence_type == "1":
        pass
    absence_duration = get_absence_duration()
    start_date = get_absence_start_date()
    if absence_duration == "4":
        end_date = get_absence_end_date()


def get_ee_id():
    """Run a while loop until the user inputs a valid employee ID,
    "menu" or "quit".

    Returns:
        str: A valid employee ID.
    """
    while True:
        print("Enter an employee ID that you want to add absence.")
        ee_id = input("Please enter here:\n").upper().strip()
        if ee_id == "MENU":
            admin_main()
            break
        elif ee_id == "QUIT":
            title.title_end()
            sys.exit()
        elif ee_id == "ADMIN":
            print("Unable to amend ADMIN data.\n")
            continue
        elif validations.validate_id(ee_id):
            return ee_id


def get_absence_type():
    """Run a while loop until the user inputs a valid digit,
    "menu" or "quit".

    Returns:
        str: A digit - 1. paid time off 2. unpaid
    """
    while True:
        print("\nPlease select an absence type.\n")
        print(f"{Fore.GREEN}1{Style.RESET_ALL} Paid Time OFF")
        print(f"{Fore.GREEN}2{Style.RESET_ALL} Unpaid Time OFF")
        absence_type = input("\nPlease enter here:\n").strip()
        if absence_type.upper() == "MENU":
            admin_main()
            break
        elif absence_type.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(absence_type, range(1, 3)):
            return absence_type


def get_absence_duration():
    """Run a while loop until the user inputs a valid digit,
    "menu" or "quit".

    Returns:
        str: A digit - 1. morning, 2. afternoon, 3. full day, 4. 2+ days
    """
    morning = "9:30AM-1:30PM"
    afternoon = "1:30PM-5:30PM"
    while True:
        print("\nPlease select a duration of the absence.\n")
        print(f"{Fore.GREEN}1{Style.RESET_ALL} {morning}")
        print(f"{Fore.GREEN}2{Style.RESET_ALL} {afternoon}")
        print(f"{Fore.GREEN}3{Style.RESET_ALL} Full day")
        print(f"{Fore.GREEN}4{Style.RESET_ALL} More than 2 consecutive days")
        choice = input("\nPlease enter a number to continue:\n").strip()
        if validations.validate_choice_number(choice, range(1, 5)):
            return choice


def get_absence_start_date():
    """Run while loop until the user inputs a valid date,
    "menu" or "quit".

    Returns:
        str: A date.
    """
    pass


def get_absence_end_date():
    """Run a while loop until the user inputs a valid data,
    "menu" or "quit".

    Returns:
        str: A date.
    """
    pass


def check_pto_hours():
    """Check unallocated hours from entitlements worksheet.

    Returns:
        str: A digit - unallocated absence entitlements.
    """
    pass


def next_move():
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid answer.
    """
    while True:
        print(f"Type {Fore.GREEN}menu{Style.RESET_ALL} to go back to the menu",
              f"or {Fore.GREEN}quit{Style.RESET_ALL} to quite the system.")
        choice = input("\nPlease enter your answer here:\n").upper().strip()
        if validations.validate_choice_letter(choice, ["MENU", "QUIT"]):
            return choice
