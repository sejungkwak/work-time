# Third-party Packages
from colorama import init, Fore, Style

# Custom Package
from worktime.app import menu, title, validations
from worktime.worksheets import requests

# colorama method to enable it on Windows
init(autoreset=True)


def admin_main():
    """Request a number between 1 and 4, the numbered options.
    Run a while loop until the user inputs a valid number.
    """
    title.title_admin()
    new_requests = requests.Requests().get_new_requests()
    if len(new_requests) > 0:
        print(f"\n{Fore.GREEN}You have",
              f"{len(new_requests)} request(s) to review.")
    else:
        print("\nThere is no more requests to review.")
    while True:
        menu.admin_menu()
        choice = input("\nPlease enter a number to continue:\n").strip()
        if validations.validate_choice_number(choice, range(1, 5)):
            break

    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    else:
        pass
