# Third-party Packages
from colorama import init, Fore, Style

# Custom Package
from worktime.app import menu, tables, title, validations
from worktime.worksheets import employees, requests

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
        review_requests()
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    else:
        pass


def requests_notification_message():
    """Check if there are new requests and display the result."""
    new_requests = requests.Requests().get_new_requests()
    if len(new_requests) > 0:
        print(f"\n{Fore.GREEN}You have",
              f"{Fore.GREEN}{len(new_requests)} request(s) to review.")
    else:
        print("\nThere is no more requests to review.")


def review_requests():
    """Display new requests and ask the user to choose a number."""
    requests_notification_message()
    new_requests = requests.Requests().get_new_requests()
    if len(new_requests) > 0:
        print("Getting data...")
        tables.display_new_requests()
        while True:
            id_list = [int(list[0]) for list in new_requests]
            print("\nEnter the ID you want to approve or reject.")
            choice = input("Please enter your answer here:\n").strip()
            if validations.validate_choice_number(choice, id_list):
                break
        action = get_action_type()


def get_action_type():
    """Run a while loop until the user types "approve" or "reject".

    Returns:
        str: User input value.
    """
    while True:
        print(f"\nEnter {Fore.GREEN}approve {Style.RESET_ALL}to approve the request",
              f"or {Fore.GREEN}reject {Style.RESET_ALL}to reject.")
        choice = input("Please enter your answer here:\n").upper().strip()
        if validations.validate_choice_letter(choice, ["APPROVE", "REJECT"]):
            return choice
