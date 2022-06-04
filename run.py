# Built-in Modules
import time

# Third-party Packages
from colorama import init, Fore, Style
from passlib.hash import pbkdf2_sha256
import stdiomask

# Custom Packages
from worktime.worksheets import (auth, clockings, credentials,
                                 entitlements, requests)
from worktime.app import tables, menu, title, utility

# colorama method to enable it on Windows
init(autoreset=True)


def validate_id():
    """Request Employee ID and validate it against Google sheet.
    Or User can choose to contact the system administrator.

    Raises:
        ValueError: If the input Employee ID is incorrect.
    """
    while True:
        try:
            print("Please enter your Employee ID.")
            print("To contact the system administrator, enter",
                  f"{Fore.GREEN}help{Style.RESET_ALL} instead.")

            ids = credentials.Credentials().ids()
            entered_id = input("\nEmployee ID:\n").upper()

            if entered_id == "HELP":
                break

            if entered_id not in ids:
                raise ValueError(
                    print("You have entered an invalid ID.")
                )

        except ValueError:
            print("Please make sure to enter your Employee ID.\n")

        else:
            return validate_pw(entered_id)
            break


def validate_pw(id):
    """Run when the user input a valid Employee ID.
    Request Password and validate it against Google sheet.

    Args:
        :id str: Employee ID that was used to log in.

    Raises:
        ValueError: If the input password is incorrect.
    """
    password = credentials.Credentials().pw(id)
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
                title.title_employee(id)
                employee_menu(id)
            break


def employee_menu(id):
    """Run a while loop to get a valid input value from the user.

    Args:
        :id str: Employee ID that was used to log in.
    """
    while True:
        menu.employee_menu()
        choice = input("\nPlease enter a number to continue:\n")
        if validate_choice(choice, range(1, 8)):
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
        pass


def validate_choice(number, options):
    """Inside the try, convert string value into integer
    and raise ValueError when the value is out of range.

    Args:
        :number str: The user input
        :options list: The number of options

    Raises:
        ValueError: If the input type is not a digit,
                    or the input value is out of range.
    """
    try:
        choice = int(number)
        if choice not in options:
            raise ValueError()
    except ValueError:
        print(f"You have entered {number}.")
        print("Please enter a correct number.")
        return False
    else:
        return True


def clock_in(id):
    """Run when the user chooses the clock in option.
    Send the clock in data to the worksheet.

    Args:
        :id str: Employee ID that was used to log in.
    """
    now = utility.get_current_datetime()
    today = now["date"]
    clock_in_at = now["time"]

    utility.clear()

    clock_sheet = clockings.Clockings(id)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(f"You already clocked out at {clocked_out_at}.")
            print(f"To update time, please contact your manager.")
        else:
            clocked_in_at = clocking["start_time"]
            is_overwrite = check_for_clockin_overwrite(clocked_in_at)
            if is_overwrite == "Y":
                clock_sheet.update_clock_in(clock_in_at)
                print(f"Clock in time has been updated: {clock_in_at}")
            else:
                print(f"Your clock in time for today: {clocked_in_at}")
    else:
        data = [id, today, clock_in_at]
        clock_sheet.add_clocking(data)
        print(f"You have successfully clocked in at {clock_in_at}.")

    print("Going back to the menu...")
    time.sleep(2)
    utility.clear()
    employee_menu(id)


def check_for_clockin_overwrite(clocked_in):
    """Run when there is clock in data already.
    Return the user answer.

    Args:
        :clocked_in str: The clocked in time
    """
    message = f"Enter {Fore.GREEN}y {Style.RESET_ALL}to overwrite "
    message += f"or {Fore.GREEN}n {Style.RESET_ALL}to go back to menu."
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
    """Run when the user chooses the clock out option.
    Send the clock out data to the worksheet.

    Args:
        :id str: Employee ID that was used to log in.
    """
    now = utility.get_current_datetime()
    today = now["date"]
    clock_out_at = now["time"]

    utility.clear()

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

    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


def display_clock_card(id):
    """Run when the user chooses the view clock card option.
    Retrieve data from the worksheet and display it.

    Args:
        :id str: Employee ID that was used to log in.
    """
    print("Clock cards display from Sunday to Saturday.")
    tables.display_clock_card(id)
    while True:
        print("If you would like to review other days,",
              "Please enter the date that you want to review.")
        print("The date should be in the following format:",
              f"{Fore.GREEN}Day/Month/Year")
        print(f"For example, {Fore.GREEN}01/12/2021",
              "for the 1st of December 2021.")
        entered_date = input("Please enter the date here:\n")
        if validate_date_input(entered_date):
            break

    if clockings.Clockings(id).get_week_clockings(entered_date):
        tables.display_clock_card(id, entered_date)
    else:
        print(f"No data found for the week of {entered_date}.")

    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


def validate_date_input(input_date):
    """Inside the try, split the values and convert them into integers
    and validate against a datetime method.

    Args:
        :input_date str: The input date

    Raises:
        ValueError: If the date is invalid.
        IndexError: If "/" is not used to separate the year, month and date.
    """
    try:
        result = utility.convert_date(input_date)
    except ValueError:
        print("Please provide the date with the correct format.")
        return False
    except IndexError:
        print("Please provide the date with the correct format.")
        return False
    else:
        return result


def display_entitlements(id):
    """Display absence entitlements for the logged in employee

    Args:
        :id str: Employee ID that was used to log in.
    """
    this_year = utility.get_current_datetime()["year"]
    utility.clear()
    print(f"\nYour absence entitlements for {this_year}.")
    tables.display_entitlements(id)

    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


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
            absence_type = check_absence_type()
        absence_start = check_absence_start_date(absence_type)
        request_id = requests.Requests().generate_req_id()
        today = utility.get_current_datetime()["date"]
        data = [request_id, id, absence_start, today, "/", "False"]
        request_days = ""
        if absence_type == "4":
            absence_end = check_absence_end_date(absence_start, unallocated)
        print(f"\n{Fore.GREEN}Your request for absence ", end="")
        if absence_type == "4":
            days = validate_days(absence_start, absence_end, unallocated)
            request_days = days
            data[3:3] = [absence_end, "", "", days]
            print(f"{Fore.GREEN}from {absence_start} to {absence_end}", end="")
        elif absence_type == "3":
            request_days = "1"
            data[3:3] = [absence_start, "", "", request_days]
            print(f"{Fore.GREEN}on {absence_start}", end="")
        else:
            request_time = ""
            request_days = "0.5"
            if absence_type == "1":
                data[3:3] = [absence_start, "9:30", "13:30", request_days]
                request_time = morning
            else:
                data[3:3] = [absence_start, "13:30", "17:30", request_days]
                request_time = afternoon
            print(f"{Fore.GREEN}on {absence_start} at {request_time}", end="")

    requests.Requests().add_request(data)
    add_pto_pending_hours(id, request_days)
    print(f"{Fore.GREEN} has been sent for review.")
    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


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
        absence_type = input("\nPlease enter a number to continue:\n")
        if validate_choice(absence_type, range(1, 5)):
            return absence_type


def check_absence_start_date(absence_type):
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
        start_date = input("Please enter the date to continue:\n")
        if validate_date_input(start_date):
            request_date = validate_date_input(start_date)
            today = utility.get_current_datetime()["date"]
            if (request_date - today).days <= 0:
                print("\nPlease note holidays must be booked in advance.")
                print("If you would like to submit absence in the past,",
                      "please contact your manager.")
            else:
                return start_date


def check_absence_end_date(start_date, unallocated):
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
        end_date = input("Please enter the date to continue:\n")
        if validate_date_input(end_date):
            if validate_days(start_date, end_date, unallocated):
                return end_date


def validate_days(date1, date2, unallocated):
    """Calculate the absence request days and hours.

    Args:
        :date1: The absence start date
        :date2: The absence end date
        :unallocated: Total available hours

    Raises:
        ValueError: If request hours are exceed the unallocated hours
                    or the end date is before start date.
    """
    try:
        start_date = validate_date_input(date1)
        end_date = validate_date_input(date2)
        num_of_days = (end_date - start_date).days + 1
        weekend = 0
        if num_of_days > 5:
            if num_of_days % 7 == 6:
                weekend = (num_of_days - num_of_days % 7) / 7 * 2 + 1
            else:
                weekend = (num_of_days - num_of_days % 7) / 7 * 2
        num_of_days -= int(weekend)
        num_of_hours = 8 * num_of_days
        if num_of_hours > float(unallocated):
            raise ValueError(
                print("Unable to complete the request.\n",
                      "You have unsufficient paid time off available:",
                      f"{unallocated}hours left.\n",
                      "Please contact your manager.")
            )
        if num_of_hours < 0:
            raise ValueError(
                print("Please make sure to enter the start",
                      "and end date correctly.")
            )
    except ValueError:
        return False
    else:
        return num_of_days


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
    can_cancel = check_cancellable(id)
    if can_cancel:
        print("Getting data...")
        allocated_absences = requests.Requests(id).get_cancellable_absence()
        tables.display_allocated_absences(id)
        while True:
            id_list = [int(list[0]) for list in allocated_absences]
            choice = input("\nPlease enter the ID you want to cancel:\n")
            if validate_choice(choice, id_list):
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

    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


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

title.title_main()
validate_id()
