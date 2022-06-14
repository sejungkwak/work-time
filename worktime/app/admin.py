"""Admin Portal module

This module provides functions to handle admin portal options.
"""

# Built-in Modules
from itertools import groupby
import sys
import time

# Custom Packages
from worktime.app import menu, messages, title, utility, validations
from worktime.app.utility import (convert_date, convert_time,
                                  get_num_of_weekdays,
                                  print_in_colour as colour)
from worktime.app.validations import (validate_choice_letter,
                                      validate_choice_number,
                                      validate_days, validate_date,
                                      validate_unpaid_days)
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
    while True:
        menu.admin_menu()
        answer = input(colour("CYAN", ">>>\n")).strip()
        utility.clear()
        if validate_choice_number(answer, range(1, 6)):
            break

    if answer == "1":
        ReviewRequests().handle_request()
    elif answer == "2":
        ReviewAttendace()
    elif answer == "3":
        AddAbsence()
    elif answer == "4":
        update_clocking()
    else:
        title.display_goodbye()
        sys.exit()


class ReviewRequests:
    """Represent Review Requests menu option."""

    def __init__(self):
        self.all_requests = requests.Requests().requests
        self.all_employees = employees.Employees().employees
        self.new_request = self.get_new_requests()
        self.new_request_notification()

    def get_new_requests(self):
        """Retrieve data that meets conditions: start date is in the future,
        not approved or rejected, not cancelled.

        Returns:
            list: A list of lists containing new request data.
        """
        today = utility.GetDatetime().tday()
        new_requests = []
        for item in self.all_requests:
            date_ = convert_date(item[2])
            if ((date_ - today).days > 0 and
                    item[-2] == "/" and item[-1] == "False"):
                new_requests.append(item)
        return new_requests

    def new_request_notification(self):
        """Check if there are new absence requests and display the result."""
        if len(self.new_request) > 0:
            word_form = "request" if len(self.new_request) == 1 else "requests"
            print(colour("YELLOW", "You have " + str(len(self.new_request))),
                  colour("YELLOW", word_form + " to review.\n"))
        else:
            print("No more requests to review right now.\n")

    def handle_request(self):
        """Call other functions to take user input
        and run a while loop until there are no new requests left."""
        num_requests = len(self.new_request)
        while num_requests > 0:
            print("Loading data...")
            utility.clear()
            self.display_new_requests()
            request_id = self.get_request_id()
            decision = self.get_decision()
            confirmed = self.get_confirm_decision(request_id, decision)
            if confirmed == "Y":
                self.update_decision(request_id, decision)
                num_requests -= 1
                for i, req in enumerate(self.new_request):
                    if req[0] == request_id:
                        self.new_request.pop(i)
            if num_requests != 0:
                print("Returning to the list...")
        menu_or_quit()

    def sort_new_request(self):
        """Sort and combine lists with the same employee ID to display
        new absence requests.

        Returns:
            new_req_list list: A list sorted by the employee ID.
        """
        # Source: mouad's answer on Stack Overflow
        # https://stackoverflow.com/questions/4174941
        self.new_request.sort(key=lambda req: req[1])
        # Source: Robert Rossney's answer on Stack Overflow
        # https://stackoverflow.com/questions/5695208
        groups = groupby(self.new_request, lambda req: req[1])
        new_req_list = [[item for item in data] for (key, data) in groups]
        return new_req_list

    def display_new_requests(self):
        """Display new absence requests grouped by employee ID."""
        sorted_new_request = self.sort_new_request()
        headers = (["ID", "Start Date", "End Date",
                    "Start Time", "End Time", "Duration"])
        for new_request in sorted_new_request:
            table = []
            for item in new_request:
                item = item[:7]
                employee_id = item.pop(1)
                fullname = get_fullname(employee_id, self.all_employees)
                item[-1] = f"{item[-1]} Day(s)"
                table.append(item)
            if len(table) > 1:
                print(f"\nNew requests from {fullname}")
            else:
                print(f"\nNew request from {fullname}")
            utility.display_table(table, headers)

    def get_request_id(self):
        """Run a while loop until the user inputs a valid request ID.

        Returns:
            str: User input value - Request ID.
        """
        while True:
            id_list = [int(item[0]) for item in self.new_request]
            print(f"\nEnter a {colour('CYAN', 'request ID')}",
                  "from the first column to approve or reject.")
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            if answer.upper() == "MENU":
                utility.clear()
                admin_main()
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_choice_number(answer, id_list):
                return answer

    @staticmethod
    def get_decision():
        """Run a while loop until the user types "approve" or "reject".

        Returns:
            str: User input value - Approve or reject.
        """
        while True:
            print(f"\nEnter {colour('CYAN', 'approve')}",
                  "to approve the request",
                  f"or {colour('CYAN', 'reject')} to reject.")
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).upper().strip()
            if answer == "MENU":
                utility.clear()
                admin_main()
                break
            if answer == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_choice_letter(answer, ["APPROVE", "REJECT"]):
                return answer

    def get_confirm_decision(self, request_id, decision):
        """Display a request review summary and ask user to confirm to proceed.

        Args:
            request_id str: Absence request ID.
            decision str: Approve or Reject.
        Returns:
            str: User input - Y or N.
        """
        for request in self.new_request:
            req_id, id_, fromdate, todate, fromtime, totime, days, *_ = request
            if req_id == request_id:
                fullname = get_fullname(id_, self.all_employees)
                if fromtime:
                    period = f"{fromtime} - {totime}"
                else:
                    period = f"{days} day" if days == "1" else f"{days} days"
        utility.clear()
        while True:
            print(colour("YELLOW", "Please confirm the details."))
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
            if validate_choice_letter(answer, ["Y", "N"]):
                return answer

    def update_decision(self, request_id, decision):
        """Update the decision to the absence_requests
        and entitlements worksheets.

        Args:
            request_id str: Request ID.
            decision str: Approve or Reject.
        """
        print("Processing...")
        employee_id, absence_days = self.get_request_details(request_id)

        # Update absence_requests worksheet
        request_sheet = requests.Requests()
        requests_row_index = int(request_id)
        hours = int(float(absence_days) * 8)
        request_sheet.update_approved(requests_row_index, decision)

        # Update entitlements worksheet
        entitle_sheet = entitlements.Entitlements(employee_id)
        if decision == "APPROVE":
            entitle_sheet.update_hours(hours, "pending_to_planned")
        else:
            entitle_sheet.update_hours(hours, "pending_to_unallocated")
        utility.clear()
        print(colour("GREEN", "Data updated successfully."))
        time.sleep(2)

    def get_request_details(self, request_id):
        """Iterate through the sheet to find the corresponding data
        to the absence request ID.

        Args:
            request_id str: Request ID on the requests worksheet.
        Returns:
            list: An employee ID and total absence days.
        """
        for request in self.new_request:
            if request_id == request[0]:
                ee_id = request[1]
                total_days = request[6]
        return [ee_id, total_days]


class ReviewAttendace:
    """Represent Review Attendace menu option."""

    def __init__(self):
        self.clock_cards = clockings.Clockings().clockings
        self.all_employees = employees.Employees().employees
        self.get_attendance_date()

    def get_attendance_date(self):
        """Display today's clock cards of all employees and then
        ask if the user wants to review other days.
        Run a while loop until they input a valid answer.
        """
        utility.clear()
        self.display_attendance()

        while True:
            print(f"\nEnter a {colour('CYAN', 'date')} to review another day.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                admin_main()
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_date(answer):
                self.display_attendance(answer)

    def display_attendance(self, date_=None):
        """Check if there is any clock in/out data, and then display the result.

        Args:
            date_ str: A DD/MM/YYYY formatted date, today if None.
        """
        utility.clear()
        today = utility.GetDatetime().tday()
        converted_date = today if date_ is None else convert_date(date_)
        text = "today" if date_ is None else date_
        headers = ["Name", "Date", "Clock In", "Clock Out"]
        table = []
        for clocking in self.clock_cards:
            ee_id, date, *_ = clocking
            if convert_date(date) == converted_date:
                for ee_ in self.all_employees:
                    if ee_id == ee_[0]:
                        # Replace the employee ID with full name
                        clocking[0] = f"{ee_[1]} {ee_[2]}"
                table.append(clocking)
            else:
                print(f"No clocking data found for {text}.")
        if table:
            print(f"Clock cards for {text}")
            utility.display_table(table, headers)


class AddAbsence:
    """Represent Add Employee Absence menu option."""

    def __init__(self):
        self.all_employees = employees.Employees().employees
        self.get_absence_data()

    def get_absence_data(self):
        """Get an employee ID, absence type(Paid or Unpaid),
        duration, start and end date from the user.
        """
        while True:
            self.ee_id = get_employee_id("to add absence.")
            self.fullname = get_fullname(self.ee_id, self.all_employees)
            entitlements_sheet = entitlements.Entitlements(self.ee_id)
            self.entitle_data = entitlements_sheet.get_entitlements()
            self.display_entitle_data()
            self.avail_hours = int(self.entitle_data[-1])
            self.absence_type = self.get_absence_type()
            self.duration = self.get_absence_duration()
            self.start_date = self.get_absence_start_date()
            if self.duration == "4":
                self.end_date = self.get_absence_end_date()
            else:
                self.end_date = self.start_date

            confirm_update = self.get_confirm_absence()
            if confirm_update == "Y":
                if self.absence_type == "1":
                    # If paid time off, update entitlements hours.
                    self.add_entitlement()
                self.add_absence()
            else:
                print(colour("GREEN", "\nNo changes were made."))
            print("\nReturning to the beginning...")
            time.sleep(3)
            utility.clear()

    def generate_absence_summary(self):
        """Generate absence start time, end time, days, depending on
        the absence type.
        """
        # Half day morning
        if self.duration == "1":
            start_time = "9:30"
            end_time = "13:30"
            days = 0.5
            period = f"{start_time} - {end_time}"
        # Half day afternoon
        elif self.duration == "2":
            start_time = "13:30"
            end_time = "17:30"
            days = 0.5
            period = f"{start_time} - {end_time}"
        # 1 full day
        elif self.duration == "3":
            start_time = ""
            end_time = ""
            days = 1
            period = "1 workday"
        # 2+ days
        else:
            start_time = ""
            end_time = ""
            days = get_num_of_weekdays(self.start_date, self.end_date)
            period = f"{days} workdays"
        return [start_time, end_time, days, period]

    def display_entitle_data(self):
        """Display the target employee's absence entitlements."""
        this_year = str(utility.GetDatetime().now_year())
        headers = ["Total", "Taken", "Planned", "Pending", "Unallocated"]
        table = [self.entitle_data]
        print(f"{self.fullname}'s absence entitlements for {this_year}")
        utility.display_table(table, headers)

    def get_absence_type(self):
        """Run a while loop until the user inputs a valid digit.

        Returns:
            str: A digit - 1. Paid time off 2. Unpaid time off.
        """
        while True:
            menu.absence_paid_menu()
            print(messages.to_menu())
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                admin_main()
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_choice_number(answer, range(1, 3)):
                if answer == "1" and self.avail_hours <= 0:
                    print(colour("RED", "Insufficient paid time " +
                                 "off available."))
                else:
                    return answer

    def get_absence_duration(self):
        """Run a while loop until the user inputs a valid digit.

        Returns:
            str: A digit - 1. Morning, 2. Afternoon, 3. A full day, 4. 2+ days
        """
        while True:
            menu.absence_period_menu()
            print(messages.to_menu())
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                admin_main()
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_choice_number(answer, range(1, 5)):
                if self.absence_type == "1":
                    if ((answer == "4" and self.avail_hours < 16) or
                            (answer == "3" and self.avail_hours < 8)):
                        print(colour("RED", "Insufficient paid time off " +
                                     "available."))
                    else:
                        return answer
                else:
                    return answer

    def get_absence_start_date(self):
        """Run while loop until the user inputs a valid date.

        Returns:
            str: A DD/MM/YYYY format date.
        """
        while True:
            if int(self.duration) in range(1, 4):
                print(f"Please enter the {colour('CYAN', 'absence date')}.")
            else:
                print(f"Please enter the {colour('CYAN', 'start date')}",
                      "for the absence duration.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                admin_main()
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_date(answer):
                request_date = convert_date(answer)
                this_year = utility.GetDatetime().now_year()
                if request_date.year != this_year and self.absence_type == "1":
                    print(messages.invalid_year())
                elif request_date.weekday() > 4:
                    print(colour("RED", "No absence updates required for " +
                                 "weekends."))
                else:
                    return answer

    def get_absence_end_date(self):
        """Run a while loop until the user inputs a valid date.

        Returns:
            str: Absence end date.
        """
        while True:
            print(f"Please enter the {colour('CYAN', 'last date')}",
                  "for the absence duration.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                admin_main()
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_date(answer):
                if ((self.absence_type == "1" and
                        validate_days(self.start_date, answer,
                                      self.avail_hours)) or
                    (self.absence_type == "2" and
                        validate_unpaid_days(self.start_date, answer))):
                    return answer

    def get_confirm_absence(self):
        """Display the absence summary and ask user to confirm to update."""
        if self.absence_type == "1":
            is_paid = "Paid absence"
        else:
            is_paid = "Unpaid absence"
        *_, period = self.generate_absence_summary()
        while True:
            print(colour("YELLOW", "Please confirm the details."))
            print(f"Employee ID: {self.ee_id}")
            print(f"Employee Name: {self.fullname}")
            print(f"Absence Type: {is_paid}")
            print(f"Start date: {self.start_date}")
            print(f"End date: {self.end_date}")
            print(f"Period: {period}")
            if self.duration == "4":
                print("Please note that weekends are not included.")
            print("\nUpdate this absence?")
            answer = input(f"{messages.y_or_n()}\n").upper().strip()
            if validate_choice_letter(answer, ["Y", "N"]):
                return answer

    def add_absence(self):
        """Update absence data to the absence_requests worksheet."""
        today = utility.GetDatetime().tday_str()
        note = today if self.absence_type == "1" else "unpaid"
        print(f"\nUpdating {self.fullname}'s absence details...")
        time.sleep(1)
        req_sheet = requests.Requests(self.ee_id)
        req_id = req_sheet.generate_req_id()
        start_time, end_time, days, *_ = self.generate_absence_summary()
        data = ([req_id, self.ee_id, self.start_date, self.end_date,
                start_time, end_time, days, note, "True", "False"])
        req_sheet.add_request(data)
        print(colour("GREEN", self.fullname + "\'s absence details " +
                     "updated successfully."))

    def add_entitlement(self):
        """Update absence data to the entitlement worksheet if paid absence."""
        print(f"\nUpdating {self.fullname}'s absence entitlements...")
        time.sleep(1)
        entitle_sheet = entitlements.Entitlements(self.ee_id)
        hours = self.generate_absence_summary()[2] * 8
        iso_start_date = convert_date(self.start_date)
        today = utility.GetDatetime().tday()
        if int((iso_start_date - today).days) > 0:
            entitle_sheet.update_hours(hours, "unallocated_to_planned")
        else:
            entitle_sheet.update_hours(hours, "unallocated_to_taken")
        print(colour("GREEN", self.fullname + "\'s absence " +
                     "entitlements updated successfully."))


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
        print(f"Enter an {colour('CYAN', 'employee ID')}",
              text)
        print(f"({messages.to_menu()})")
        answer = input(colour("CYAN", ">>>\n")).upper().strip()
        utility.clear()
        if answer == "MENU":
            admin_main()
            break
        if answer == "QUIT":
            title.display_goodbye()
            sys.exit()
        elif answer == "ADMIN":
            print(colour("RED", "Unable to amend ADMIN data.\n"))
            continue
        elif validations.validate_id(answer, ids):
            return answer


def update_clocking():
    """Get user input for updating clockings sheet(employee ID, date,
    clock in or out, time) and update accordingly.
    Run a while loop until user types menu or quit.
    """
    all_employees = employees.Employees().employees
    while True:
        id_ = get_employee_id("to update clock cards.")
        date_ = get_date()
        fullname = get_fullname(id_, all_employees)
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
            print(colour("GREEN", "Data updated successfully."))
        else:
            print(colour("GREEN", "No changes were made."))
        print("\nReturning to the beginning...")
        time.sleep(2)


def get_date():
    """Run while loop until the user inputs a valid date.

    Returns:
        str: A DD/MM/YYYY format date.
    """
    while True:
        print(f"Enter a {colour('CYAN', 'date')} to update.")
        print(messages.date_format())
        print(f"({messages.to_menu()})")
        answer = input(colour("CYAN", ">>>\n")).strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        if answer.upper() == "QUIT":
            title.display_goodbye()
            sys.exit()
        elif validate_date(answer):
            today = utility.GetDatetime().tday()
            if convert_date(answer) > today:
                print(colour("RED", "Unable to set clocking time " +
                             "in the future."))
            elif convert_date(answer).month != today.month:
                print(colour("RED", "Unable to update clocking time " +
                             "after payroll has been processed."))
            else:
                date_ = convert_date(answer).strftime("%d/%m/%Y")
                return date_


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
        utility.display_table(table, headers)
    else:
        print(colour("YELLOW", "No clock in / out data found for"),
              colour("YELLOW", id_ + f"({fullname}) on {date_}.\n"))
    while True:
        menu.update_clocking_menu()
        print(f"({messages.to_menu()})")
        answer = input(colour("CYAN", ">>>\n")).strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        if answer.upper() == "QUIT":
            title.display_goodbye()
            sys.exit()
        elif validate_choice_number(answer, range(1, 3)):
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
        *_, from_time, to_time = data.values()
    while True:
        print(f"Enter {colour('CYAN', 'time')} to update",
              f"{colour('CYAN', 'clock ' + type_.lower())} time.")
        print("The time should be in the 24-hour notation:",
              f"{colour('CYAN', 'Hour:Minute')}.")
        print("For example, 9:00 is the nine o\'clock in the morning",
              "and 17:00 is the five o\'clock in the evening.")
        print(f"({messages.to_menu()})")
        answer = input(colour("CYAN", ">>>\n")).strip()
        utility.clear()
        if answer.upper() == "MENU":
            admin_main()
            break
        if answer.upper() == "QUIT":
            title.display_goodbye()
            sys.exit()
        elif validations.validate_time(answer):
            if type_ == "IN" and data is not None and to_time != "":
                if convert_time(answer) >= convert_time(to_time):
                    print(colour("RED", "Clock in time must be " +
                          "before clock out time."))
                else:
                    return answer
            elif type_ == "OUT" and data is not None and from_time != "":
                if convert_time(answer) <= convert_time(from_time):
                    print(colour("RED", "Clock out time must be " +
                          "after clock in time."))
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
        print(colour("YELLOW", "Please confirm the details."))
        print(f"Employee ID: {id_}")
        print(f"Employee Name: {fullname}")
        print(f"Update Date: {date_}")
        print(f"Clocking Type: Clock {in_out}")
        print(f"Update Time: {time_}")
        print("\nUpdate?")
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        utility.clear()
        if validate_choice_letter(answer, ["Y", "N"]):
            return answer


def get_fullname(id_, employee_list):
    """Returns an employee's full name.

    Args:
        id_: An employee ID.
        employee_list: A list of all employees
    """
    for employee in employee_list:
        if employee[0] == id_:
            fullname = f"{employee[1]} {employee[2]}"
    return fullname


def menu_or_quit():
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid answer.

    Returns:
        str: The user input - menu or quit.
    """
    while True:
        print(messages.to_menu())
        answer = input(colour("CYAN", ">>>\n")).upper().strip()
        utility.clear()
        if validate_choice_letter(answer, ["MENU", "QUIT"]):
            if answer == "MENU":
                admin_main()
                break
            title.display_goodbye()
            sys.exit()
