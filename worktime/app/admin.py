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
        get_absence_data()
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
        print("There are no more requests to review right now.")


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
        print(utility.green("Data updated successfully."))
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
        print(f"\nEnter a {utility.cyan('request ID')}",
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
        print(f"\nEnter {utility.cyan('approve')}",
              "to approve the request",
              f"or {utility.cyan('reject')} to reject.")
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
        print(f"Clock cards for {date}")
        tables.display_table(headers, table)
    return data


def get_absence_data():
    """Get an employee ID, absence type(Paid or Unpaid),
    duration, start and end date from the user.
    """
    ee_id = get_employee_id()
    avail_hours = int(get_avail_hours(ee_id))
    absence_type = get_absence_type(avail_hours)
    absence_duration = get_absence_duration(absence_type, avail_hours)
    start_date = get_absence_start_date(absence_type, absence_duration)
    if absence_duration == "4":
        end_date = get_absence_end_date(absence_type, start_date, avail_hours)
    else:
        end_date = start_date
    get_confirm_absence(ee_id, absence_type, start_date, end_date,
                        absence_duration)


def get_confirm_absence(id, type, from_date, to_date, duration):
    """Display the absence summary and ask user to confirm to update.

    Args:
        id str: An employee ID.
        type str: 1. Paid, 2. Unpaid.
        from_date str: The absence start date - DD/MM/YYYY.
        to_date str: The absence end date - DD/MM/YYYY.
        duration str: 1. morning, 2. afternoon, 3. full day, 4. 2+ days
    """
    fullname = employees.Employees(id).get_fullname()
    start_time = ""
    end_time = ""
    total_hours = 4
    is_paid = "Paid absence" if type == "1" else "Unpaid absence"
    if duration == "1":
        period = "9:30 - 13:30"
    elif duration == "2":
        period = "13:30 - 17:30"
    elif duration == "3":
        period = "1 day"
        total_hours = 8
    else:
        period = utility.get_num_of_weekdays(from_date, to_date)
        total_hours = period * 8
        period = f"{period} days"

    while True:
        utility.clear()
        print(f"{utility.yellow('Please confirm the details.')}")
        print(f"Employee ID: {id}")
        print(f"Employee Name: {fullname}")
        print(f"Absence Type: {is_paid}")
        print(f"Start date: {from_date}")
        print(f"End date: {to_date}")
        print(f"Period: {period}")
        if duration == "4":
            print("Please note that the weekends are not included.")
        print("\nUpdate this absence?")
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            if answer == "Y":
                if type == "1":
                    add_entitlement(id, from_date, total_hours, fullname)
                add_absence(id, from_date, to_date, duration, total_hours,
                            fullname)
                break
            else:
                print(utility.green('No changes were made.'))
                print("Returning to the menu...")
                time.sleep(2)
                utility.clear()
                admin_main()
                break


def add_absence(id, from_date, to_date, duration, hours, fullname):
    """Update absence data to the absence_requests worksheet.

    Args:
        id str: An employee ID.
        from_date str: The absence start date - DD/MM/YYYY.
        to_date str: The absence end date - DD/MM/YYYY.
        duration str: 1. morning, 2. afternoon, 3. full day, 4. 2+ days
        hours int: Total number of the absence hours.
        fullname str: An employee name.
    """
    print(f"\nUpdating {fullname}'s absence details...")
    time.sleep(1)
    req_sheet = requests.Requests(id)
    req_id = req_sheet.generate_req_id()
    days = hours / 8
    start_time = ""
    end_time = ""
    if duration == "1":
        start_time = "9:30"
        end_time = "13:30"
    if duration == "2":
        start_time = "13:30"
        end_time = "17:30"
    data = ([req_id, id, from_date, to_date,
            start_time, end_time, days, "", "True", "False"])
    req_sheet.add_request(data)
    print(utility.green(fullname + "\'s absence details"),
          utility.green("updated successfully."))

    menu_quit = menu_or_quit()
    utility.clear()
    if menu_quit == "MENU":
        admin_main()
    else:
        title.title_end()
        sys.exit()


def add_entitlement(id, from_date, hours, fullname):
    """Update absence data to the entitlement worksheet if paid absence.

    Args:
        id str: An employee ID.
        from_date str: The absence start date - DD/MM/YYYY.
        hours int: Total number of the absence hours.
        fullname str: An employee name.
    """
    print(f"\nUpdating {fullname}'s absence entitlements...")
    time.sleep(1)
    entitle_sheet = entitlements.Entitlements(id)
    iso_start_date = utility.convert_date(from_date)
    if int((iso_start_date - utility.get_today()).days) > 0:
        entitle_sheet.update_hours(hours, "unallocated_to_planned")
    else:
        entitle_sheet.update_hours(hours, "unallocated_to_taken")
    print(utility.green(fullname + "\'s absence entitlements"),
          utility.green("updated successfully."))


def get_employee_id():
    """Run a while loop until the user inputs a valid employee ID.

    Returns:
        str: A valid employee ID.
    """
    while True:
        utility.clear()
        print(f"Enter an {utility.cyan('employee ID')}",
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
            print(f"{utility.red('Unable to amend ADMIN data.')}\n")
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
        utility.clear()
        menu.absence_paid_menu()
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
                print(utility.red("Insufficient paid time off available."))
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
        utility.clear()
        menu.absence_period_menu()
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
                    print(utility.red("Insufficient paid time off available."))
                else:
                    return answer
            else:
                return answer


def get_absence_start_date(type, duration):
    """Run while loop until the user inputs a valid date.

    Args:
        type str: Absence type - Paid or unpaid time off.
        duration str: Absence duration - 1 & 2. Half day, 3. A day, 4. 2+ days
    Returns:
        str: A DD/MM/YYYY format date.
    """
    utility.clear()
    while True:
        if int(duration) in range(1, 4):
            print("\nPlease enter the absence date.")
        else:
            print(f"\nPlease enter the {utility.cyan('start date')}",
                  "for the absence duration.")
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
            if type == "1" and
            answer[-4:] != str(utility.get_current_datetime()["year"]):
                print(messages.invalid_year())
            else:
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
    utility.clear()
    while True:
        print(f"\nPlease enter the {utility.cyan('last date')}",
              "for the absence duration.")
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
            if ((type == "1" and
                    validations.validate_days(date, answer, hours)) or
                    (type == "2" and
                        validations.validate_unpaid_days(date, answer))):
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
