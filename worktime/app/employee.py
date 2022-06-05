# Built-in Modules
import sys

# Third-party Packages
from colorama import init, Fore, Style

# Custom Packages
from worktime.worksheets import clockings, entitlements, requests
from worktime.app import menu, tables, title, utility, validations

# colorama method to enable it on Windows
init(autoreset=True)


def employee_menu(id):
    """Request a number between 1 and 7, the numbered options.
    Run a while loop until the user inputs a valid number.

    Args:
        :id str: Employee ID that was used to log in.
    """
    while True:
        menu.employee_menu()
        choice = input("\nPlease enter a number to continue:\n").strip()
        if validations.validate_choice_number(choice, range(1, 8)):
            break

    if choice == "1":
        clock_in(id)
    elif choice == "2":
        clock_out(id)
    elif choice == "3":
        display_clock_card(id)
    elif choice == "4":
        display_entitlements(id)
    elif choice == "5":
        book_absence(id)
    elif choice == "6":
        cancel_absence(id)
    else:
        title.title_end()
        sys.exit()


def clock_in(id):
    """Run when the user chooses the clock in option.
    Send the clock in data to the worksheet.

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    now = utility.get_current_datetime()
    today = now["date"]
    clock_in_at = now["time"]
    clock_sheet = clockings.Clockings(id)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(f"You already clocked out at {clocked_out_at}.")
            print(f"To update time, please contact your manager.")
        else:
            clocked_in_at = clocking["start_time"]
            print(f"\nYou already clocked in for today at {clocked_in_at}.")
            print(f"Would you like to overwrite it?")
            is_overwrite = check_for_clockin_overwrite()
            if is_overwrite == "Y":
                clock_sheet.update_clock_in(clock_in_at)
                print(f"Clock in time has been updated: {clock_in_at}")
            else:
                print(f"Your clock in time for today: {clocked_in_at}")
    else:
        data = [id, today, clock_in_at]
        clock_sheet.add_clocking(data)
        print(f"You have successfully clocked in at {clock_in_at}.")
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        employee_menu(id)
    else:
        title.title_end()
        sys.exit()


def check_for_clockin_overwrite():
    """Run when there is clock in data already.
    Return the user answer.
    """
    while True:
        print(f"Enter {Fore.GREEN}y {Style.RESET_ALL}to overwrite",
              f"or {Fore.GREEN}n {Style.RESET_ALL}to go back to the menu.")
        answer = input("\nPlease enter your answer here:\n").upper().strip()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            return answer


def clock_out(id):
    """Run when the user chooses the clock out option.
    Send the clock out data to the worksheet.

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    now = utility.get_current_datetime()
    today = now["date"]
    clock_out_at = now["time"]
    clock_sheet = clockings.Clockings(id)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(f"{Fore.RED}You already clocked out at {clocked_out_at}.")
            print("Please contact your manager",
                  "to update your clock out time.")
        else:
            clock_sheet.update_clock_out(clock_out_at)
            print(f"You have successfully clocked out at {clock_out_at}.")
    else:
        data = [id, today, "", clock_out_at]
        clock_sheet.add_clocking(data)
        print(f"{Fore.RED}You did not clock in today.")
        print("Please contact your manager to add your clock in time.")
        print(f"You have successfully clocked out at {clock_out_at}.")
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        employee_menu(id)
    else:
        title.title_end()
        sys.exit()


def display_clock_card(id):
    """Run when the user chooses the view clock card option.
    Retrieve data from the worksheet and display it.

    Args:
        :id str: Employee ID that was used to log in.
    """
    clock_sheet = clockings.Clockings(id)
    if clock_sheet.get_week_clockings():
        print("Your Clock card for this week.")
        print("Clock cards display from Sunday to Saturday.")
        tables.display_clock_card(id)
    else:
        print("No data found for this week.")
    while True:
        print("\nIf you would like to review other days,",
              "please enter the date that you want to review.")
        print("The date should be in the following format:",
              f"{Fore.GREEN}Day/Month/Year")
        print(f"For example, {Fore.GREEN}01/12/2021",
              "for the 1st of December 2021.")
        entered_date = input("Please enter the date here:\n").strip()
        if validations.validate_date(entered_date):
            break

    if clock_sheet.get_week_clockings(entered_date):
        tables.display_clock_card(id, entered_date)
    else:
        print(f"No data found for the week of {entered_date}.")
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        employee_menu(id)
    else:
        title.title_end()
        sys.exit()


def display_entitlements(id):
    """Display absence entitlements for the logged in employee

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    this_year = utility.get_current_datetime()["year"]
    print(f"\nYour absence entitlements for {this_year}.")
    tables.display_entitlements(id)
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        employee_menu(id)
    else:
        title.title_end()
        sys.exit()


def book_absence(id):
    """Run when the user select book absence menu

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    unallocated = entitlements.Entitlements(id).get_entitlements()[-1]
    morning = "9:30AM-1:30PM"
    afternoon = "1:30PM-5:30PM"

    if unallocated == "0":
        print("You do not have paid time off available.")
        print("Please contact your manager.")
    else:
        print(f"\nYou have {unallocated} hours available to book absence.")
        absence_type = check_absence_type()
        if ((absence_type == "4" and float(unallocated) < 16) or
                (absence_type == "3" and float(unallocated) < 8)):
            print("You have unsufficient paid time off available",
                  "to complete the request.")
            print("Please select a different option or",
                  "contact your manager.")
        fromdate = get_absence_start_date(absence_type)
        request_id = requests.Requests().generate_req_id()
        today = utility.get_current_datetime()["date"]
        data = [request_id, id, fromdate, today, "/", "False"]
        request_days = ""
        if absence_type == "4":
            todate = get_absence_end_date(fromdate, unallocated)
        print(f"\n{Fore.GREEN}Your request for absence ", end="")
        if absence_type == "4":
            days = validations.validate_days(fromdate, todate, unallocated)
            request_days = days
            data[3:3] = [todate, "", "", days]
            print(f"{Fore.GREEN}from {fromdate} to {todate}", end="")
        elif absence_type == "3":
            request_days = "1"
            data[3:3] = [fromdate, "", "", request_days]
            print(f"{Fore.GREEN}on {fromdate}", end="")
        else:
            request_time = ""
            request_days = "0.5"
            if absence_type == "1":
                data[3:3] = [fromdate, "9:30", "13:30", request_days]
                request_time = morning
            else:
                data[3:3] = [fromdate, "13:30", "17:30", request_days]
                request_time = afternoon
            print(f"{Fore.GREEN}on {fromdate} at {request_time}", end="")
    print(f"{Fore.GREEN} is being submitted...")
    requests.Requests().add_request(data)
    add_pto_pending_hours(id, request_days)
    print(f"{Fore.GREEN}Your request has been sent for review.")
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        employee_menu(id)
    else:
        title.title_end()
        sys.exit()


def check_absence_type():
    """Ask user to choose an option for the absence duration."""
    morning = "9:30AM-1:30PM"
    afternoon = "1:30PM-5:30PM"
    while True:
        print("\nPlease select an option that is the most suitable",
              "for your absence duration.\n")
        print(f"{Fore.GREEN}1{Style.RESET_ALL} {morning}")
        print(f"{Fore.GREEN}2{Style.RESET_ALL} {afternoon}")
        print(f"{Fore.GREEN}3{Style.RESET_ALL} Full day")
        print(f"{Fore.GREEN}4{Style.RESET_ALL} More than 2 consecutive days")
        absence_type = input("\nPlease enter a number to continue:\n").strip()
        if validations.validate_choice_number(absence_type, range(1, 5)):
            return absence_type


def get_absence_start_date(absence_type):
    """Ask user to input the absence (start) date.

    Args:
        :absence_type str: Absence duration
            1. morning, 2. afternoon, 3. full day, 4. 2+ days
    """
    while True:
        if int(absence_type) in range(1, 4):
            print("\nPlease enter a date that you want to book.")
        else:
            print("\nPlease enter the start date that you want to book.")
        print("The date should be in the following format:",
              f"{Fore.GREEN}Day/Month/Year")
        print(f"For example, {Fore.GREEN}01/12/2021",
              "for the 1st of December 2021.")
        start_date = input("Please enter the date to continue:\n").strip()
        if validations.validate_date(start_date):
            request_date = validations.validate_date(start_date)
            today = utility.get_current_datetime()["date"]
            today = utility.convert_date(today)
            request_year = request_date.year
            this_year = int(utility.get_current_datetime()["year"])
            if (request_date - today).days <= 0:
                print(f"{Fore.YELLOW}\nPlease note holidays must be",
                      f"{Fore.YELLOW}booked in advance.")
                print(f"{Fore.YELLOW}If you would like to submit absence in",
                      f"{Fore.YELLOW}the past, please contact your manager.")
            elif request_year != this_year:
                print(f"{Fore.YELLOW}\nUnable to process your request.")
                print(f"{Fore.YELLOW}Absence entitlements must be",
                      f"{Fore.YELLOW}taken within the leave year.")
            else:
                return start_date


def get_absence_end_date(start_date, unallocated):
    """Ask user to input absence end date if they are booking 2+ days.

    Args:
        :start_date str: The absence start date.
        :unallocated str: The number of available absence hours.
    """
    while True:
        print("\nPlease enter the end date for your absence duration.")
        print("The date should be in the following format:",
              f"{Fore.GREEN}Day/Month/Year")
        print(f"For example, {Fore.GREEN}01/12/2021",
              "for the 1st of December 2021.")
        end_date = input("Please enter the date to continue:\n").strip()
        if validations.validate_date(end_date):
            if validations.validate_days(start_date, end_date, unallocated):
                return end_date


def add_pto_pending_hours(id, days):
    """Update pending value on the entitlements worksheet.

    Args:
        :id str: Employee ID that was used to log in.
        :days str: The number of requested absence days.
    """
    entitlement = entitlements.Entitlements(id)
    hours = int(float(days) * 8)

    entitlement.update_hours("pending", hours, "add")
    entitlement.update_hours("unallocated", hours, "substract")


def cancel_absence(id):
    """Update absence_requests and entitlements worksheets.

    Args:
        :id str: Employee ID that was used to log in.
    """
    utility.clear()
    can_cancel = check_cancellable(id)
    if can_cancel:
        print("Getting data...")
        allocated_absences = requests.Requests(id).get_cancellable_absence()
        tables.display_allocated_absences(id)
        while True:
            id_list = [int(list[0]) for list in allocated_absences]
            choice = input("Please enter the ID you want to cancel:\n").strip()
            if validations.validate_choice_number(choice, id_list):
                break
        print("Processing...")
        row_index = int(choice) + 1
        requests.Requests().update_cancelled(row_index)
        absence_days = requests.Requests().get_duration(row_index)
        is_approved = requests.Requests().get_approved(row_index)
        absence_hours = int(float(absence_days) * 8)
        entitlement = entitlements.Entitlements(id)
        if is_approved == "True":
            entitlement.update_hours("planned", absence_hours, "subtract")
        else:
            entitlement.update_hours("pending", absence_hours, "subtract")
        entitlement.update_hours("unallocated", absence_hours, "add")
        print("Your absence has been successfully cancelled.")
    sequence = next_move()
    utility.clear()
    if sequence == "MENU":
        employee_menu(id)
    else:
        title.title_end()
        sys.exit()


def check_cancellable(id):
    """Search if the user has planned/pending absence.

    Args:
        :id str: Employee ID that was used to log in.
    """
    entitlement = entitlements.Entitlements(id)
    planned = entitlement.get_hours("planned")
    pending = entitlement.get_hours("pending")
    if planned == pending == 0:
        print("You do not have any planned/pending absence to cancel.")
        return False
    else:
        return True


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
