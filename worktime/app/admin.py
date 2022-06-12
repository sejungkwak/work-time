# Built-in Modules
import sys
import time
from itertools import groupby

# Custom Packages
from worktime.app import menu, messages, tables, title, utility, validations
from worktime.worksheets import (clockings, credentials, employees,
                                 entitlements, requests)


def admin_main():
    """Request a number between 1 and 5, the numbered options:
        1. Review Requests
        2. Review Attendance
        3. Add Employee Absence
        4. Update Clock Card
        5. Exit
    Run a while loop until the user inputs a valid number.
    """
    all_requests = requests.Requests().requests
    new_request = get_new_requests(all_requests)
    new_request_notification(new_request)
    while True:
        menu.admin_menu()
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
        if validations.validate_choice_number(answer, range(1, 6)):
            break

    if answer == "1":
        handle_request(new_request)
    elif answer == "2":
        ReviewAttendace().get_attendance_date()
    elif answer == "3":
        get_absence_data()
    elif answer == "4":
        update_clocking()
    else:
        title.title_end()
        sys.exit()


def get_new_requests(data):
    """Retrieve data that meets conditions: start date is in the future,
    not approved or rejected, not cancelled.

    Args:
        data list: The absence_requests worksheet values.
    Returns:
        list: A list of lists containing new request data.
    """
    today = utility.GetDatetime().tday()
    new_requests = []
    for item in data:
        date_ = utility.convert_date(item[2])
        if ((date_ - today).days > 0 and
                item[-2] == "/" and not eval(item[-1])):
            new_requests.append(item)
    return new_requests


def handle_request(new_request):
    """Display new requests and take user input.
    Run a while loop until there are no new requests left.

    Args:
        new_request list: A list of lists containing new absence requests.
    """
    new_request_notification(new_request)
    num_requests = len(new_request)
    while num_requests > 0:
        print("Loading data...")
        request_list = sort_new_request(new_request)
        utility.clear()
        tables.display_new_requests(request_list)
        req_id = get_request_id(new_request)
        decision = get_decision()
        confirmed = get_confirm_decision(req_id, new_request, decision)
        if confirmed == "Y":
            num_requests -= 1
            update_decision(req_id, new_request, decision)
            for i, req in enumerate(new_request):
                if req[0] == req_id:
                    new_request.pop(i)
        if num_requests > 0:
            print("Returning to the list...")
    else:
        menu_or_quit()


def get_confirm_decision(req_id, requests_, decision):
    """Display a request review summary and ask user to confirm to proceed.

    Args:
        req_id str: Request ID.
        requests_ list: A list of lists containing all new requests.
        decision str: Approve or Reject.
    Returns:
        str: User input - Y or N.
    """
    for request in requests_:
        if request[0] == req_id:
            req_id, id_, fromdate, todate, fromtime, totime, days, *_ = request
            fullname = employees.Employees(id_).get_fullname()
            if fromtime:
                period = f"{fromtime} - {totime}"
            else:
                period = f"{days} day" if days == "1" else f"{days} days"
    utility.clear()
    while True:
        print(f"{utility.yellow('Please confirm the details.')}")
        print(f"Employee ID: {id_}")
        print(f"Employee Name: {fullname}")
        print(f"Start date: {fromdate}")
        print(f"End date: {todate}")
        print(f"Period: {period}")
        if decision == "APPROVE":
            print("\nApprove this request?")
        else:
            print("\nReject this request?")
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        utility.clear()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            return answer


def update_decision(req_id, requests_, decision):
    """Update the absence_requests and entitlements worksheets
    depending on the user input(approve or reject).

    Args:
        req_id str: Request ID.
        requests_ list: A list of lists containing all new requests.
        decision str: Approve or Reject.
    """
    print("Processing...")
    employee_id = find_ee_id(req_id, requests_)
    requests_row_index = int(req_id)

    request_sheet = requests.Requests()
    absence_days = request_sheet.get_duration(requests_row_index)
    hours = int(float(absence_days) * 8)
    request_sheet.update_approved(requests_row_index, decision)

    entitle_sheet = entitlements.Entitlements(employee_id)
    if decision == "APPROVE":
        entitle_sheet.update_hours(hours, "pending_to_planned")
    else:
        entitle_sheet.update_hours(hours, "pending_to_unallocated")
    utility.clear()
    print(utility.green("Data updated successfully."))
    time.sleep(2)


def new_request_notification(new_request):
    """Check if there are new absence requests and display the result.

    Args:
        new_request list: A list of lists containing new absence requests.
    """
    if len(new_request) > 0:
        word_form = "request" if len(new_request) == 1 else "requests"
        print(f"{utility.yellow('You have ' + str(len(new_request)))}",
              f"{utility.yellow(word_form + ' to review.')}\n")
    else:
        print("No more requests to review right now.\n")


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


def get_request_id(new_request):
    """Run a while loop until the user inputs a valid value.

    Args:
        new_request list: A list of list containing new absence requests.
    Returns:
        str: User input value - Request ID.
    """
    while True:
        id_list = [int(item[0]) for item in new_request]
        print(f"\nEnter a {utility.cyan('request ID')}",
              "from the first column to approve or reject.")
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
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
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").upper().strip()
        if answer == "MENU":
            admin_main()
            break
        elif answer == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_letter(answer, ["APPROVE", "REJECT"]):
            return answer


def find_ee_id(request_id, new_request):
    """Iterate through the sheet to find the corresponding employee ID
    to the request ID.

    Args:
        request_id str: Request ID on the requests worksheet.
        new_request list: A list of lists containing new absence requests.
    Returns:
        str: An employee ID.
    """
    for request in new_request:
        if request_id == request[0]:
            ee_id = request[1]
            return ee_id


class ReviewAttendace:
    """Represent Review Attendace menu option."""

    def __init__(self):
        self.clock_cards = clockings.Clockings().clockings
        self.all_employees = employees.Employees().employees

    def get_attendance_date(self):
        """Display today's clock cards of all employees and then
        ask if the user wants to review other days.
        Run a while loop until they input a valid answer.
        """
        utility.clear()
        self.display_attendance()

        while True:
            print(f"\nEnter a {utility.cyan('date')} to review another day.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(f"{utility.cyan('>>>')}\n").strip()
            utility.clear()
            if answer.upper() == "MENU":
                admin_main()
                break
            elif answer.upper() == "QUIT":
                title.title_end()
                sys.exit()
            elif validations.validate_date(answer):
                if len(answer) != 10:
                    print(utility.red("Invalid format: " + answer))
                else:
                    self.display_attendance(answer)

    def display_attendance(self, date_=None):
        """Check if there is any clock in/out data, and then display the result.

        Args:
            date_ str: A DD/MM/YYYY formatted date, today if None.
        """
        print("Getting clocking data...")
        today = utility.GetDatetime().tday_str()
        date_ = today if date_ is None else date_
        headers = ["Name", "Date", "Clock In", "Clock Out"]
        table = []
        for clocking in self.clock_cards:
            ee_id, date, clock_in, clock_out = clocking
            if date == date_:
                for ee in self.all_employees:
                    if ee_id == ee[0]:
                        fullname = f"{ee[1]} {ee[2]}"
                clocking[0] = fullname
                table.append(clocking)
            else:
                utility.clear()
                print(f"No clocking data found for {date_}.")
        if table:
            utility.clear()
            print(f"Clock cards for {date_}")
            tables.display_table(table, headers)


def get_absence_data():
    """Get an employee ID, absence type(Paid or Unpaid),
    duration, start and end date from the user.
    """
    ee_id = get_employee_id("to add absence.")
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
    total_hours = 4
    is_paid = "Paid absence" if type == "1" else "Unpaid absence"
    if duration == "1":
        period = "9:30 - 13:30"
    elif duration == "2":
        period = "13:30 - 17:30"
    elif duration == "3":
        period = "1 workday"
        total_hours = 8
    else:
        period = utility.get_num_of_weekdays(from_date, to_date)
        total_hours = period * 8
        period = f"{period} workdays"

    while True:
        print(f"{utility.yellow('Please confirm the details.')}")
        print(f"Employee ID: {id}")
        print(f"Employee Name: {fullname}")
        print(f"Absence Type: {is_paid}")
        print(f"Start date: {from_date}")
        print(f"End date: {to_date}")
        print(f"Period: {period}")
        if duration == "4":
            print("Please note that weekends are not included.")
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
                utility.clear()
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

    menu_or_quit()


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
    today = utility.GetDatetime().tday()
    if int((iso_start_date - today).days) > 0:
        entitle_sheet.update_hours(hours, "unallocated_to_planned")
    else:
        entitle_sheet.update_hours(hours, "unallocated_to_taken")
    print(utility.green(fullname + "\'s absence entitlements"),
          utility.green("updated successfully."))


def get_employee_id(text):
    """Run a while loop until the user inputs a valid employee ID.

    Args:
        text str: Purpose of the ID request.
    Returns:
        str: A valid employee ID.
    """
    utility.clear()
    ids = credentials.Credentials().ids()
    while True:
        print(f"Enter an {utility.cyan('employee ID')}",
              text)
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").upper().strip()
        utility.clear()
        if answer == "MENU":
            admin_main()
            break
        elif answer == "QUIT":
            title.title_end()
            sys.exit()
        elif answer == "ADMIN":
            print(f"{utility.red('Unable to amend ADMIN data.')}\n")
            continue
        elif validations.validate_id(answer, ids):
            return answer


def get_absence_type(hours):
    """Run a while loop until the user inputs a valid digit.

    Args:
        hours int: Available paid time off hours.
    Returns:
        str: A digit - 1. Paid time off 2. Unpaid time off.
    """
    utility.clear()
    while True:
        menu.absence_paid_menu()
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
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
        menu.absence_period_menu()
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
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
            print(f"\nPlease enter the {utility.cyan('absence date')}.")
        else:
            print(f"\nPlease enter the {utility.cyan('start date')}",
                  "for the absence duration.")
        print(messages.date_format())
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_date(answer):
            request_date = utility.convert_date(answer)
            this_year = str(utility.GetDatetime().now_year())
            if answer[-4:] != this_year and type == "1":
                print(messages.invalid_year())
            elif request_date.weekday() > 4:
                print(utility.red("No absence updates required for weekends."))
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
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
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


def update_clocking():
    """Get user input for updating clockings sheet(employee ID, date,
    clock in or out, time) and update accordingly.
    Run a while loop until user types menu or quit.
    """
    while True:
        id_ = get_employee_id("to update clock cards.")
        date_ = get_date()
        fullname = employees.Employees(id_).get_fullname()
        data = clockings.Clockings(id_).get_one_clocking(date_)
        in_or_out = clock_in_or_out(id_, date_, fullname, data)
        time_ = get_time(data, in_or_out)
        confirm = get_confirm_clocking(id_, date_, in_or_out, time_, fullname)
        if confirm == "Y":
            print(f"Updating clock {in_or_out.lower()} time...")
            clocking_sheet = clockings.Clockings(id_)
            if data is None and in_or_out == "IN":
                clocking_sheet.add_clocking([id_, date_, f"{time_}:00", ""])
            elif data is None and in_or_out == "OUT":
                clocking_sheet.add_clocking([id_, date_, "", f"{time_}:00"])
            elif data and in_or_out == "IN":
                clocking_sheet.update_clock_in(date_, f"{time_}:00")
            else:
                clocking_sheet.update_clock_out(date_, f"{time_}:00")
            print(utility.green("Data updated successfully."))
            print("Returning to the beginning...")
            time.sleep(2)
        else:
            print(utility.green("No changes were made."))
            print("Returning to the beginning...")
            time.sleep(2)


def get_date():
    """Run while loop until the user inputs a valid date.

    Returns:
        str: A DD/MM/YYYY format date.
    """
    while True:
        print(f"Enter a {utility.cyan('date')} to update.")
        print(messages.date_format())
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_date(answer):
            today = utility.GetDatetime().tday()
            today_str = utility.GetDatetime().tday_str()
            if utility.convert_date(answer) > today:
                print(utility.red("Unable to set clocking time"),
                      utility.red("in the future."))
            elif answer[3:5] != today_str[3:5]:
                print(utility.red("Unable to update clocking time"),
                      utility.red("after payroll has been processed."))
            else:
                return answer


def clock_in_or_out(id_, date_, fullname, data):
    """Display the target employee's clock card for the target date to update.
    Run while loop until the user inputs a valid input:
    1 for clock in update or 2 for clock out update.

    Args:
        id_ str: An employee ID.
        date_ str: A %d/%m/%Y format date.
        fullname str: Employee's name.
        data dict: Clocking data.
    Returns:
        str: IN or OUT from user input.
    """
    if data is not None:
        print(f"{id_}\'s clock card")
        table = ([[fullname, data["date"], data["start_time"],
                 data["end_time"]]])
        headers = ["Name", "Date", "Clock In", "Clock Out"]
        tables.display_table(table, headers)
    else:
        print(utility.yellow("No clock in / out data found for"),
              utility.yellow(f"{id_}({fullname}) on {date_}.\n"))
    while True:
        menu.update_clocking_menu()
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(answer, range(1, 3)):
            in_out = "IN" if answer == "1" else "OUT"
            return in_out


def get_time(data, type_):
    """Run while loop until the user inputs a valid time.

    Args:
        data dict: Clocking data or None.
        type_ str: IN or OUT for clock in or clock out.
    Returns:
        str: A %H:%M format time.
    """
    if data is not None:
        row, id, date, from_time, to_time = data.values()
    while True:
        print(f"Enter {utility.cyan('time')} to update",
              f"{utility.cyan('clock ' + type_.lower())} time.")
        print("The time should be in the 24-hour notation:",
              f"{utility.cyan('Hour:Minute')}.")
        print("For example, 9:00 is the nine o\'clock in the morning",
              "and 17:00 is the five o\'clock in the evening.")
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_time(answer):
            if type_ == "IN" and data is not None and to_time != "":
                if (utility.convert_time(answer) >=
                        utility.convert_time(to_time)):
                    print(utility.red("Clock in time must be"),
                          utility.red("before clock out time."))
                else:
                    return answer
            elif type_ == "OUT" and data is not None and from_time != "":
                if (utility.convert_time(answer) <=
                        utility.convert_time(from_time)):
                    print(utility.red("Clock out time must be"),
                          utility.red("after clock in time."))
                else:
                    return answer
            else:
                return answer


def get_confirm_clocking(id_, date_, in_out, time_, fullname):
    """Display a clock card update summary and ask user to confirm to proceed.

    Args:
        id_ str: An employee ID.
        date_ str: A %d/%m/%Y format date.
        in_out str: IN or OUT for clock in or clock out.
        time_ str: A %H:%M format time.
        fullname str: Employee's name.
    Returns:
        str: User input - Y or N.
    """
    in_out = in_out.capitalize()
    while True:
        print(f"{utility.yellow('Please confirm the details.')}")
        print(f"Employee ID: {id_}")
        print(f"Employee Name: {fullname}")
        print(f"Update Date: {date_}")
        print(f"Clocking Type: Clock {in_out}")
        print(f"Update Time: {time_}")
        print("\nUpdate?")
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        utility.clear()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            return answer


def menu_or_quit():
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid answer.

    Returns:
        str: The user input - menu or quit.
    """
    while True:
        print(messages.to_menu())
        answer = input(f"{utility.cyan('>>>')}\n").upper().strip()
        utility.clear()
        if validations.validate_choice_letter(answer, ["MENU", "QUIT"]):
            if answer == "MENU":
                admin_main()
                break
            else:
                title.title_end()
                sys.exit()
