# Built-in Modules
from datetime import date
from os import name, system
import time

# Third-party Packages
from art import *
from colorama import init, Fore, Style
from passlib.hash import pbkdf2_sha256
import stdiomask
from tabulate import tabulate

# Custom Package
from worktime.worksheets import auth, employees

# colorama method to enable it on Windows
init(autoreset=True)

cred_sheet = auth.SHEET.worksheet("login_credentials")
login_credentials = cred_sheet.get_all_values()


# Source: https://www.geeksforgeeks.org/clear-screen-python/
def clear():
    """Clear the screen."""
    system("cls" if name == "nt" else "clear")


def welcome_message():
    """Display the application name and welcome message."""
    clear()
    tprint("Work Time".center(29), font="tarty7")
    print("\n" + "Welcome to Work Time - Time Management System".center(80))
    print("\n" + "="*80 + "\n")


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

            ids = [id for id, password in login_credentials]
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
    password_col = 2
    row_index = cred_sheet.find(id).row
    password = cred_sheet.cell(row_index, password_col).value

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
    """Return the current date and time in dictionary."""
    local_time = time.localtime()
    get_year = time.strftime("%Y", local_time)
    get_date = time.strftime("%d/%m/%Y", local_time)
    get_time = time.strftime("%H:%M:%S", local_time)
    return {"year": get_year, "date": get_date, "time": get_time}


def run_employee_portal(id):
    """Display the title and welcome message for the employee portal.

    Args:
        :id str: Employee ID that was used to log in.
    """
    name = employees.Employees(id).get_fname()
    clear()
    tprint("Employee Portal".center(18), font="rectangles")
    print(f"Welcome back, {name}!".center(80))
    print("\n" + "="*80)


def employee_menu(id):
    """Run a while loop to get a valid input value from the user.

    Args:
        :id str: Employee ID that was used to log in.
    """
    while True:
        print("\nPlease choose one of the following options.\n")
        print(f"{Fore.GREEN}1{Style.RESET_ALL} Clock In")
        print(f"{Fore.GREEN}2{Style.RESET_ALL} Clock Out")
        print(f"{Fore.GREEN}3{Style.RESET_ALL} View Clock Card")
        print(f"{Fore.GREEN}4{Style.RESET_ALL} View Absence Entitlements")
        print(f"{Fore.GREEN}5{Style.RESET_ALL} Book Absence")
        print(f"{Fore.GREEN}6{Style.RESET_ALL} Cancel Absence")
        print(f"{Fore.GREEN}7{Style.RESET_ALL} Log Out")
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
    now = get_datetime()
    today = now["date"]
    clock_in_at = now["time"]

    clock_sheet = auth.SHEET.worksheet("clockings")
    clockings = clock_sheet.get_all_values()
    clear()
    for row_index, clocking in enumerate(clockings, start=1):
        user_id, date, clocked_in, clocked_out = clocking

        if id == user_id and today == date and clocked_in:
            is_overwrite = check_for_clockin_overwrite(clocked_in)
            if is_overwrite == "Y":
                clock_in_col = 3
                clock_sheet.update_cell(row_index, clock_in_col, clock_in_at)
                print(f"Clock in time has been updated: {clock_in_at}")
                break
            else:
                break
    else:
        data = [id, today, clock_in_at]
        clock_sheet.append_row(data)
        print(f"You have successfully clocked in at {clock_in_at}.")

    print("Going back to the menu...")
    time.sleep(2)
    clear()
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
    now = get_datetime()
    today = now["date"]
    clock_out_at = now["time"]

    clock_sheet = auth.SHEET.worksheet("clockings")
    clockings = clock_sheet.get_all_values()
    clear()
    for clocking in clockings:
        user_id, date, clocked_in, clocked_out = clocking
        if id == user_id and today == date:
            if clocked_out:
                print(f"{Fore.RED}You have already",
                      f"{Fore.RED}clocked out at {clocked_out}.")
                print("Please contact your manager",
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


def display_clock_card(id):
    """Run when the user chooses the view clock card option.
    Retrieve data from the worksheet and display it.

    Args:
        :id str: Employee ID that was used to log in.
    """
    clock_sheet = auth.SHEET.worksheet("clockings")
    clockings = clock_sheet.get_all_values()

    while True:
        print("Please enter the date that you want to review.")
        print("The date should be in the following format:",
              f"{Fore.GREEN}Day/Month/Year")
        print(f"For example, {Fore.GREEN}01/12/2021",
              "for the 1st of December 2021.")
        entered_date = input("Please enter the date here:\n")
        if validate_date_input(entered_date):
            break

    for clocking in clockings:
        user_id, date, clocked_in, clocked_out = clocking
        if id == user_id and entered_date == date:
            table = [[date, clocked_in, clocked_out]]
            headers = ["Date", "Clock In", "Clock Out"]
            print(tabulate(table, headers, tablefmt="fancy_grid"))
            break
    else:
        print(f"No data found for {entered_date}.")

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
        date_to_list = input_date.split("/")
        entered_year = int(date_to_list[2])
        entered_month = int(date_to_list[1])
        entered_date = int(date_to_list[0])
        result = date(entered_year, entered_month, entered_date)
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
    this_year = get_datetime()["year"]
    entitlement_sheet = auth.SHEET.worksheet("entitlements")
    row_index = entitlement_sheet.find(id).row
    entitlements = entitlement_sheet.row_values(row_index)[1:]
    table = [[entitlement for entitlement in entitlements]]
    headers = ["Total Hours", "Taken", "Planned", "Pending", "Unallocated"]
    clear()
    print(f"\nYour absence entitlements for {this_year}.")
    print(tabulate(table, headers, tablefmt="fancy_grid"))

    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


def book_absence(id):
    """Run when the user select book absence menu

    Args:
        :id str: Employee ID that was used to log in.
    """
    clear()
    entitlement_sheet = auth.SHEET.worksheet("entitlements")
    absence_sheet = auth.SHEET.worksheet("absence_requests")
    row_index = entitlement_sheet.find(id).row
    entitlements = entitlement_sheet.row_values(row_index)
    unallocated = entitlements[-1]
    morning = "9:30AM.-1:30PM."
    afternoon = "1:30PM.-5:30PM."

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
        request_id = create_absence_request_id()
        today = get_datetime()["date"]
        data = [request_id, id, absence_start]
        request_days = ""
        if absence_type == "4":
            absence_end = check_absence_end_date(absence_start, unallocated)
        print(f"\n{Fore.GREEN}Your request for absence ", end="")
        if absence_type == "4":
            days = validate_days(absence_start, absence_end, unallocated)
            request_days = days
            data.extend([absence_end, "", "", days])
            print(f"{Fore.GREEN}from {absence_start} to {absence_end}", end="")
        elif absence_type == "3":
            request_days = "1"
            data.extend([absence_start, "", "", request_days])
            print(f"{Fore.GREEN}on {absence_start}", end="")
        else:
            request_time = ""
            request_days = "0.5"
            if absence_type == "1":
                data.extend([absence_start, "9:30", "13:30", request_days])
                request_time = morning
            else:
                data.extend([absence_start, "13:30", "17:30", request_days])
                request_time = afternoon
            print(f"{Fore.GREEN}on {absence_start} at {request_time}", end="")

    data.extend([today, "/", "False"])
    absence_sheet.append_row(data)
    add_pto_pending_hours(id, request_days)
    print(f"{Fore.GREEN} has been sent for review.")
    time.sleep(2)
    print("Going back to the menu...")
    time.sleep(2)
    employee_menu(id)


def check_absence_type():
    """Ask user to choose an option for the absence duration."""
    morning = "9:30AM.-1:30PM."
    afternoon = "1:30PM.-5:30PM."
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
            today = date.today()
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


def create_absence_request_id():
    """Increment the request id by 1.
    If there hasn't been a request, assign 1 to it.
    """
    absence_sheet = auth.SHEET.worksheet("absence_requests")
    request_id = absence_sheet.col_values(1)[-1]
    if request_id == "request_id":
        request_id = "1"
    else:
        request_id = int(request_id) + 1
    return request_id


def add_pto_pending_hours(id, days):
    """Update pending value on the entitlements worksheet.

    Args:
        :id str: Employee ID that was used to log in.
        :days str: The number of requested absence days.
    """
    entitlement_sheet = auth.SHEET.worksheet("entitlements")
    pending_col = 5
    unallocated_col = 6
    row_index = entitlement_sheet.find(id).row
    pending = entitlement_sheet.cell(row_index, pending_col).value
    unallocated = entitlement_sheet.cell(row_index, unallocated_col).value
    hours = float(days) * 8
    pending_hour = float(pending) + float(hours)
    unallocated_hour = float(unallocated) - float(hours)

    entitlement_sheet.update_cell(row_index, pending_col, pending_hour)
    entitlement_sheet.update_cell(row_index, unallocated_col, unallocated_hour)


def cancel_absence(id):
    """Update absence_requests and entitlements worksheets.

    Args:
        :id str: Employee ID that was used to log in.
    """
    can_cancel = check_cancellable(id)
    if can_cancel:
        print("Getting data...")
        allocated_absences = get_cancellable_absence(id)
        display_allocated_absences(allocated_absences)

        while True:
            id_list = [int(list[0]) for list in allocated_absences]
            choice = input("\nPlease enter the ID you want to cancel:\n")
            if validate_choice(choice, id_list):
                break
        print("Processing...")
        absence_sheet = auth.SHEET.worksheet("absence_requests")
        entitlement_sheet = auth.SHEET.worksheet("entitlements")
        row_index = int(choice) + 1
        duration_col = 7
        approved_col = 9
        cancelled_col = "J"
        absence_sheet.update(f"{cancelled_col}{row_index}", "True", raw=True)
        absence_days = absence_sheet.cell(row_index, duration_col).value
        is_approved = absence_sheet.cell(row_index, approved_col).value
        absence_hours = int(absence_days) * 8
        id_row = entitlement_sheet.find(id).row
        planned_col = 4
        pending_col = 5
        unallocated_col = 6
        pending_hours = entitlement_sheet.cell(id_row, pending_col).value
        pending_hours = int(pending_hours) - absence_hours
        available_hours = entitlement_sheet.cell(id_row, unallocated_col).value
        available_hours = int(available_hours) + absence_hours
        if is_approved.capitalize() == "True":
            entitlement_sheet.update_cell(id_row, planned_col, pending_hours)
        else:
            entitlement_sheet.update_cell(id_row, pending_col, pending_hours)
        entitlement_sheet.update_cell(id_row, unallocated_col, available_hours)
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
    entitlement_sheet = auth.SHEET.worksheet("entitlements")
    row_index = entitlement_sheet.find(id).row
    planned_col = 4
    pending_col = 5
    planned = entitlement_sheet.cell(row_index, planned_col).value
    pending = entitlement_sheet.cell(row_index, pending_col).value
    if planned == "0" and pending == "0":
        print("You do not have any planned/pending absence to cancel.")
        return False
    else:
        return True


def get_cancellable_absence(id):
    """Return a list of lists containing cancellable absence data.

    Args:
        :id str: Employee ID that was used to log in.
    """
    absence_sheet = auth.SHEET.worksheet("absence_requests")
    get_cells = absence_sheet.findall(id)

    row_indices = []
    for cell in get_cells:
        row_indices.append(cell.row)

    requests = []
    for index in row_indices:
        request = absence_sheet.row_values(index)
        start_date = request[2]
        start_date = validate_date_input(start_date)
        today = get_datetime()["date"]
        today = validate_date_input(today)
        is_approved = request[8].capitalize()
        is_cancelled = eval(request[9])

        if ((start_date - today).days > 0 and
                (is_approved == "True" or is_approved == "/") and
                not is_cancelled):
            requests.append(request)

    return requests


def display_allocated_absences(data):
    """Display absence requests that can be cancelled by the user.

    Args:
        :data list:
    """
    absence_lists = []
    for list in data:
        list = list[:7]
        list[-1] = f"{list[-1]} Day(s)"
        list.pop(1)
        absence_lists.append(list)
    headers = (["ID", "Start Date", "End Date",
                "Start Time", "End Time", "Duration"])
    print(tabulate(absence_lists, headers, tablefmt="fancy_grid"))

welcome_message()
validate_id()
