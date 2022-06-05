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
        render_requests()
    elif choice == "2":
        render_attendance()
    elif choice == "3":
        pass
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


def render_requests():
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


def render_attendance():
    """Check if there is any clock in/out data from the worksheet and 
    call display_clock_card to display the data.
    """
    all_ees = employees.Employees()
    ee_ids = [ee[0] for ee in all_ees.employees]
    print("Clock cards display from Monday to Sunday.")
    for ee_id in ee_ids:
        clock_sheet = clockings.Clockings(ee_id)
        if clock_sheet.get_week_clockings():
            tables.display_clock_card(ee_id)
        else:
            print(f"No data found for this week for {ee_id}.")


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
