# Built-in Modules
import sys
import time
from itertools import groupby

# Custom Package
from worktime.app import menu, messages, tables, title, utility, validations
from worktime.worksheets import clockings, employees, entitlements, requests


def admin_main():
    """Request a number between 1 and 4, the numbered options:
        1. Review Requests
        2. Review Attendance
        3. Add Employee Absence
        4. Log Out
    Run a while loop until the user inputs a valid number.
    """
    while True:
        menu.admin_menu()
        answer = input(f"\n{messages.enter_number()}\n").strip()
        if validations.validate_choice_number(answer, range(1, 5)):
            break

    if answer == "1":
        handle_request()
    elif answer == "2":
        get_attendance_date()
    elif answer == "3":
        add_absence()
    else:
        title.title_end()
        sys.exit()


def new_request_notification():
    """Check if there are new requests and display the result."""
    new_request = requests.Requests().get_new_requests()
    if len(new_request) > 0:
        word_form = "request" if len(new_request) == 1 else "requests"
        print(f"\n{utility.yellow('You have ' + str(len(new_request)))}",
              f"{utility.yellow(word_form + ' to review.')}")
    else:
        print("\nThere are no more requests to review right now.")


def handle_request():
    """Display new requests and update the worksheet depending on the user
    input - approve or reject.
    """
    new_request_notification()
    new_request = requests.Requests().get_new_requests()
    if len(new_request) > 0:
        print("Getting data...")
        request_list = sort_new_request(new_request)
        tables.display_new_requests(request_list)
        req_id = get_request_id()
        decision = get_decision()
        print("Processing...")
        time.sleep(3)
        utility.clear()
        requests_row_index = int(req_id)
        requests.Requests().update_approved(requests_row_index, decision)
        employee_id = find_ee_id(req_id)
        absence_days = requests.Requests().get_duration(requests_row_index)
        hours = int(float(absence_days) * 8)
        entitle_sheet = entitlements.Entitlements(employee_id)
        if decision == "APPROVE":
            entitle_sheet.update_hours(hours, "pending_to_planned")
        else:
            entitle_sheet.update_hours(hours, "pending_to_unallocated")
        print("Data has been updated successfully.")
    menu_quit = menu_or_quit()
    utility.clear()
    if menu_quit == "MENU":
        admin_main()
    else:
        title.title_end()
        sys.exit()


def sort_new_request(req_list):
    """Sort and combine lists with the same employee ID to display
    new absence requests.

    Args:
        req_list list: A list of lists containing new requests.
    Returns:
        new_req_list list: A list sorted by the employee ID.
    """
    # Source: mouad's answer on Stack Overflow
    # https://stackoverflow.com/questions/4174941
    req_list.sort(key=lambda req: req[1])
    # Source: Robert Rossney's answer on Stack Overflow
    # https://stackoverflow.com/questions/5695208
    groups = groupby(req_list, lambda req: req[1])
    new_req_list = [[item for item in data] for (key, data) in groups]
    return new_req_list


def get_request_id():
    """Run a while loop until the user inputs a valid value.

    Returns:
        str: User input value - Request ID.
    """
    new_request = requests.Requests().get_new_requests()
    while True:
        id_list = [int(item[0]) for item in new_request]
        print(f"\nEnter a {utility.green('request ID')}",
              "from the first column to approve or reject.")
        print(messages.to_menu())
        answer = input(f"{messages.enter_req_id()}\n").strip()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(answer, id_list):
            return answer


def get_decision():
    """Run a while loop until the user types "approve" or "reject".

    Returns:
        str: User input value - Approve or reject.
    """
    while True:
        print(f"\nEnter {utility.green('approve')}",
              "to approve the request",
              f"or {utility.green('reject')} to reject.")
        print(messages.to_menu())
        answer = input("Enter approve or reject here:\n").upper().strip()
        if answer == "MENU":
            admin_main()
            break
        elif answer == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_letter(answer, ["APPROVE", "REJECT"]):
            return answer


def find_ee_id(request_id):
    """Iterate through the sheet to find the corresponding employee ID
    to the request ID.

    Args:
        request_id str: Request ID on the requests worksheet.
    Returns:
        str: An employee ID.
    """
    new_request = requests.Requests().requests
    for request in new_request:
        if request_id == request[0]:
            ee_id = request[1]
            return ee_id


def get_attendance_date():
    """Display today's clock cards of all employees and then ask if the user wants
    to review other days. Run a while loop until they input a valid answer.
    """
    utility.clear()
    if not display_attendance():
        print("There is no clocking data for today.")

    while True:
        print("\nEnter a date to review another day.")
        print(messages.date_format())
        print(messages.to_menu())
        answer = input(f"{messages.enter_date()}\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        else:
            if validations.validate_date(answer):
                utility.clear()
                display_attendance(answer)


def display_attendance(date=None):
    """Check if there is any clock in/out data, and then display the result.

    Args:
        date str: A DD/MM/YYYY formatted date. Today if none.
    Returns:
        bool: True if there are clock cards.
    """
    utility.clear()
    print("Getting clocking data...")
    today = utility.get_current_datetime()["date"]
    date = today if date is None else date
    data = False
    no_data = ""
    headers = ["Name", "Date", "Clock In", "Clock Out"]
    table = []
    clock_sheet = clockings.Clockings()
    cards = clock_sheet.get_one_all_employee(date)
    if cards:
        for card in cards:
            card[0] = employees.Employees(card[0]).get_fullname()
            table.append(card)
        data = True
    else:
        utility.clear()
        print(f"There is no clocking data for {date}.")
    if table:
        utility.clear()
        print(f"Clock cards for {date}.")
        tables.display_table(headers, table)
    return data


def add_absence():
    """Get an employee ID, absence type(1 - Paid, 2 - Unpaid),
    duration(1&2 - half day, 3 - a day, 4 - 2+ days),
    start and end date from the user and update data to worksheet.
    """
    ee_id = get_employee_id()
    avail_hours = int(get_avail_hours(ee_id))
    absence_type = get_absence_type(avail_hours)
    absence_duration = get_absence_duration(absence_type, avail_hours)
    start_date = get_absence_start_date(absence_duration)

    end_date = start_date
    start_time = ""
    end_time = ""
    total_hours = 4
    if absence_duration == "1":
        start_time = "9:30"
        end_time = "13:30"
    elif absence_duration == "2":
        start_time = "13:30"
        end_time = "17:30"
    elif absence_duration == "3":
        total_hours = 8
    else:
        end_date = get_absence_end_date(absence_type, start_date, avail_hours)
        total_hours = utility.get_num_of_weekdays(start_date, end_date) * 8

    if absence_type == "1":
        entitle_sheet = entitlements.Entitlements(ee_id)
        iso_start_date = utility.convert_date(start_date)
        if int((iso_start_date - utility.get_today()).days) > 0:
            entitle_sheet.update_hours(total_hours, "unallocated_to_planned")
        else:
            entitle_sheet.update_hours(total_hours, "unallocated_to_taken")
    req_sheet = requests.Requests(ee_id)
    req_id = req_sheet.generate_req_id()
    days = total_hours / 8
    data = ([req_id, ee_id, start_date, end_date,
            start_time, end_time, days, "", "True", "False"])
    req_sheet.add_request(data)


def get_employee_id():
    """Run a while loop until the user inputs a valid employee ID.

    Returns:
        str: A valid employee ID.
    """
    while True:
        print(f"Enter an {utility.green('employee ID')}",
              "to add absence.")
        print(messages.to_menu())
        answer = input(f"{messages.enter_ee_id()}\n").upper().strip()
        if answer == "MENU":
            admin_main()
            break
        elif answer == "QUIT":
            title.title_end()
            sys.exit()
        elif answer == "ADMIN":
            print("Unable to amend ADMIN data.\n")
            continue
        elif validations.validate_id(answer):
            return answer


def get_absence_type(hours):
    """Run a while loop until the user inputs a valid digit.

    Args:
        hours int: Available paid time off hours.
    Returns:
        str: A digit - 1. Paid time off 2. Unpaid time off.
    """
    while True:
        print("\nPlease select an absence type.\n")
        print(f"{utility.green('1')} Paid Time OFF")
        print(f"{utility.green('2')} Unpaid Time OFF")
        print(messages.to_menu())
        answer = input(f"\n{messages.enter_number()}\n").strip()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(answer, range(1, 3)):
            if answer == "1" and hours <= 0:
                print("Insufficient paid time off available.")
            else:
                return answer


def get_absence_duration(type, hours):
    """Run a while loop until the user inputs a valid digit.

    Args:
        type str: Absence type - Paid or unpaid time off.
        hours int: Available paid time off hours.
    Returns:
        str: A digit - 1. Morning, 2. Afternoon, 3. A full day, 4. 2+ days
    """
    while True:
        menu.absence_menu()
        print(messages.to_menu())
        answer = input(f"\n{messages.enter_number()}\n").strip()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(answer, range(1, 5)):
            if type == "1":
                if ((answer == "4" and hours < 16) or
                        (answer == "3" and hours < 8)):
                    print("Insufficient paid time off available.")
                else:
                    return answer
            else:
                return answer


def get_absence_start_date(duration):
    """Run while loop until the user inputs a valid date.

    Args:
        duration str: Absence duration - 1 & 2. Half day, 3. A day, 4. 2+ days
    Returns:
        str: A DD/MM/YYYY format date.
    """
    while True:
        if int(duration) in range(1, 4):
            print("\nPlease enter the absence date.")
        else:
            print("\nPlease enter the start date for the absence duration.")
        print(messages.date_format())
        print(messages.to_menu())
        answer = input(f"{messages.enter_date()}\n").strip()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_date(answer):
            return answer


def get_absence_end_date(type, date, hours):
    """Run a while loop until the user inputs a valid date.

    Args:
        type str: 1(Paid time off) or 2(Unpaid time off).
        date str: A DD/MM/YYYY format absence start date.
        hours str: Total available absence hours.
    Returns:
        str: Absence end date.
    """
    while True:
        print("\nPlease enter the last date for the absence duration.")
        print(messages.date_format())
        answer = input(f"{messages.enter_date()}\n").strip()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_date(answer):
            if ((type == "1" and
                    validations.validate_days(answer, date, hours)) or
                    (type == "2" and
                        validations.validate_unpaid_days(answer, date))):
                break
        return answer


def get_avail_hours(id):
    """Get paid time off hours from the entitlements worksheet.

    Args:
        id str: An employee ID.
    Returns:
        str: A digit - Paid time off hours.
    """
    entitle_sheet = entitlements.Entitlements(id)
    avail_hours = entitle_sheet.get_hours("unallocated")
    return avail_hours


def menu_or_quit():
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid answer.

    Returns:
        str: The user input - menu or quit.
    """
    while True:
        print(messages.to_menu())
        answer = input(f"\n{messages.enter_menu()}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["MENU", "QUIT"]):
            return answer
