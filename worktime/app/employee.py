"""Employee Portal module

This module provides functions to handle employee portal options.
"""

# Built-in Modules
import sys
import time

# Custom Packages
from worktime.app import menu, messages, title, utility
from worktime.app.utility import get_num_of_weekdays, print_in_colour as colour
from worktime.app.validations import (validate_choice_letter,
                                      validate_choice_number,
                                      validate_days, validate_date)
from worktime.worksheets import clockings, entitlements, requests


def employee_main(id_):
    """Request a number between 1 and 7, the numbered options.
        1. Clock In
        2. Clock Out
        3. View Clock Card
        4. View Absence Entitlements
        5. Book Absence
        6. Cancel Absence
        7. Exit
    Run a while loop until the user inputs a valid number.

    Args:
        id_ str: Employee ID that was used to log in.
    """
    while True:
        menu.employee_menu()
        choice = input(colour("CYAN", ">>>\n")).strip()
        utility.clear()
        if validate_choice_number(choice, range(1, 8)):
            break

    if choice == "1":
        clock_in(id_)
    elif choice == "2":
        clock_out(id_)
    elif choice == "3":
        ViewClockCard(id_)
    elif choice == "4":
        display_entitlements(id_)
    elif choice == "5":
        BookAbsence(id_)
    elif choice == "6":
        CancelAbsence(id_)
    else:
        title.display_goodbye()
        sys.exit()


def clock_in(id_):
    """Run when the user chooses the clock in option.
    Send the clock in data to the worksheet.

    Args:
        id_ str: Employee ID that was used to log in.
    """
    today = utility.GetDatetime().tday_str()
    clock_in_at = utility.GetDatetime().now_time_str()
    clock_sheet = clockings.Clockings(id_)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(colour("RED", id_ + " already clocked out at " +
                  clocked_out_at + "."))
            print("To update the clock in time, contact a manager.\n")
        else:
            clocked_in_at = clocking["start_time"]
            print(colour("YELLOW", id_ + " already clocked in for today at " +
                  clocked_in_at + "."))
            print("Overwrite it?")
            answer = check_for_overwrite()
            utility.clear()
            if answer == "Y":
                clock_sheet.update_clock_in(today, clock_in_at)
                print(colour("GREEN", "Clock in time has been " +
                      "updated to " + clock_in_at + ".\n"))
            else:
                print(colour("GREEN", "No changes were made.\n"))
    else:
        data = [id_, today, clock_in_at]
        clock_sheet.add_clocking(data)
        print(colour("GREEN", "Successfully clocked in at " +
              clock_in_at + ".\n"))
    menu_or_quit(id_)


def check_for_overwrite():
    """Run a while loop until the user inputs a valid value.

    Returns:
        str: The user input - Y or N
    """
    while True:
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        if validate_choice_letter(answer, ["Y", "N"]):
            return answer


def clock_out(id_):
    """Check if there is clocking data for today already and update worksheet.

    Args:
        id_ str: Employee ID that was used to log in.
    """
    today = utility.GetDatetime().tday_str()
    clock_out_at = utility.GetDatetime().now_time_str()
    clock_sheet = clockings.Clockings(id_)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(colour("RED", id_ + " already clocked out at " +
                  clocked_out_at + '.'))
            print("To update the clock out time contact a manager.\n")
        else:
            clock_sheet.update_clock_out(today, clock_out_at)
            print(colour("GREEN", "Successfully clocked out at " +
                  clock_out_at + ".\n"))
    else:
        data = [id_, today, "", clock_out_at]
        clock_sheet.add_clocking(data)
        print(colour("RED", "No clock in data for today."))
        print(colour("RED", "To add the clock in tiem, " +
              "contact a manager.\n"))
        print(colour("GREEN", "Successfully clocked out at"),
              colour("GREEN", clock_out_at + ".\n"))
    menu_or_quit(id_)


class ViewClockCard:
    """Represent View Clock Card menu option.

    Args:
        id_ str: Employee ID that was used to log in.
    """

    def __init__(self, id_):
        self.id_ = id_
        self.attendance_data = clockings.Clockings().clockings
        self.today = utility.GetDatetime().tday_str()
        self.display_attendance()
        self.get_attendance_date()

    def get_attendance_date(self):
        """Ask the user input a date to review other weeks clock cards.
        Run a while loop until they input a valid answer.
        """
        while True:
            print(
                f"\nEnter a {colour('CYAN', 'date')} to review another week.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(self.id_)
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_date(answer):
                utility.clear()
                self.display_attendance(answer)

    def display_attendance(self, date_=None):
        """Check if there is any clock in/out data, and then display the result.

        Args:
            date_ str: A DD/MM/YYYY formatted date. Today if none.
        """
        utility.clear()
        text = "this week" if date_ is None else f"the week of {date_}"
        date_ = self.today if date_ is None else date_
        headers = ["ID", "Date", "Clock In", "Clock Out"]
        table = self.get_week_clockings(date_)
        utility.clear()
        if table:
            print(f"Clock cards for {text}.")
            utility.display_table(table, headers)
        else:
            print(f"No clocking data found for {text}.\n")

    def get_week_clockings(self, date_=None):
        """Iterate through the sheet to find week's values that match the date.

        Args:
            date_ str: A DD/MM/YYYY formatted date. Today if none.
        """
        date_ = self.today if date_ is None else date_
        date_ = utility.convert_date(date_)
        dates = utility.get_week(date_, "week")
        result = []
        for day in dates:
            for clocking in self.attendance_data:
                ee_id, date, *_ = clocking
                if ee_id == self.id_ and date == day:
                    result.append(clocking)
        return result


def display_entitlements(id_):
    """Display absence entitlements for the logged in employee.

    Args:
        id_ str: Employee ID that was used to log in.
    """
    this_year = utility.GetDatetime().now_year()
    data = entitlements.Entitlements(id_).get_entitlements()
    table = [[item for item in data]]
    headers = ["Total Hours", "Taken", "Planned", "Pending", "Unallocated"]
    print(f"Absence entitlements for {this_year}.")
    utility.display_table(table, headers)
    print("\n", end="")
    menu_or_quit(id_)


class BookAbsence:
    """Represent Book Absence menu option.

    Args:
        id_ str: Employee ID that was used to log in.
    """

    def __init__(self, id_):
        self.id_ = id_
        self.unallocated = entitlements.Entitlements(
            id_).get_entitlements()[-1]
        self.avail_hours = int(self.unallocated)
        self.book_absence()

    def book_absence(self):
        """Get absence request data from a user.
        Run a while loop until no available paid time off hours left.
        """
        while self.avail_hours > 0:
            self.display_avail_hours()
            self.duration = self.get_duration()
            self.start_date = self.get_start_date()
            if self.duration == 4:
                self.end_date = self.get_end_date()
            else:
                self.end_date = self.start_date

            self.confirm = self.get_confirm_request()
            if self.confirm == "Y":
                self.add_absence_request()
                self.add_pending_hours()
                hours = self.generate_absence_summary()[2] * 8
                self.avail_hours -= hours
            else:
                print(colour("GREEN", "No requests were submitted."))
            print("\nReturning to the beginning...")
            time.sleep(3)
            utility.clear()
        self.display_avail_hours()
        menu_or_quit(self.id_)

    def generate_absence_summary(self):
        """Generate absence start time, end time, days, depending on
        the absence type.
        """
        # Half day morning
        if self.duration == 1:
            start_time = "9:30"
            end_time = "13:30"
            days = 0.5
            period = f"{start_time} - {end_time}"
        # Half day afternoon
        elif self.duration == 2:
            start_time = "13:30"
            end_time = "17:30"
            days = 0.5
            period = f"{start_time} - {end_time}"
        # 1 full day
        elif self.duration == 3:
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

    def display_avail_hours(self):
        """Display the employee's available paid time off hours."""
        if self.avail_hours == 0:
            print(colour("RED", "Insufficient paid time off available " +
                  "to book absence.\n"))
        else:
            print(f"{self.avail_hours} hours available to book absence.")

    def get_duration(self):
        """Ask user to choose an option for the absence duration.
        Run a while loop until the user input is between 1 and 4, and
        not exceeding their available paid time off hours.

        Return:
            int: User input if successful.
                 1(9:30AM-1:30PM), 2(1:30PM-5:30PM), 3(Full day), 4(2+ days)
        """
        while True:
            menu.absence_period_menu()
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(self.id_)
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_choice_number(answer, range(1, 5)):
                if ((answer == "4" and self.avail_hours < 16) or
                        (answer == "3" and self.avail_hours < 8)):
                    print(colour("RED", "Insufficient paid time off " +
                          "available to complete the request."))
                    print("Select a different option or contact a manager.")
                else:
                    return int(answer)

    def get_start_date(self):
        """Ask user to input the absence (start) date.

        Return:
            str: User input if successful.
        """
        while True:
            if self.duration in range(1, 4):
                print(f"\nEnter the {colour('CYAN', 'absence date')}.")
            else:
                print(f"\nEnter the {colour('CYAN', 'start date')}",
                      "for the absence duration.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            if answer.upper() == "MENU":
                utility.clear()
                employee_main(self.id_)
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_date(answer):
                request_date = utility.convert_date(answer)
                today = utility.GetDatetime().tday()
                request_year = request_date.year
                this_year = utility.GetDatetime().now_year()
                if (request_date - today).days <= 0:
                    print(colour("RED", "\nPlease note holidays must be " +
                          "booked in advance."))
                    print("To submit absence in the past, contact a manager.")
                elif request_year != this_year:
                    print(messages.invalid_year())
                elif request_date.weekday() > 4:
                    print(colour("RED", "No absence requests required for " +
                          "weekends."))
                else:
                    return answer

    def get_end_date(self):
        """Ask user to input absence end date if they are booking 2+ days.

        Return:
            str: User input if successful.
        """
        while True:
            print(f"\nEnter the {colour('CYAN', 'last date')}",
                  "for the absence duration.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            if answer.upper() == "MENU":
                utility.clear()
                employee_main(self.id_)
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif (validate_date(answer) and
                    validate_days(self.start_date, answer, self.avail_hours)):
                return answer

    def get_confirm_request(self):
        """Display absence request summary and ask user to confirm to submit.

        Returns:
            str: User input - Y or N.
        """
        *_, period = self.generate_absence_summary()
        while True:
            utility.clear()
            print(colour("YELLOW", "Please confirm the absence request."))
            print(f"Start date: {self.start_date}")
            print(f"End date: {self.end_date}")
            print(f"Period: {period}")
            if self.duration == 4:
                print("Please note that weekends are not included.")
            print("\nSubmit this request?")
            answer = input(f"{messages.y_or_n()}\n").upper().strip()
            utility.clear()
            if validate_choice_letter(answer, ["Y", "N"]):
                return answer

    def add_absence_request(self):
        """Update the absence_requests worksheet."""
        print("Submitting your absence request...\n")
        request_sheet = requests.Requests()
        req_id = request_sheet.generate_req_id()
        today = utility.GetDatetime().tday_str()
        start_time, end_time, days, *_ = self.generate_absence_summary()
        data = ([req_id, self.id_, self.start_date, self.end_date,
                 start_time, end_time, days, today, "/", "False"])
        request_sheet.add_request(data)
        print(colour("GREEN", "Absence request submitted successfully."))
        time.sleep(3)

    def add_pending_hours(self):
        """Update the entitlements worksheet."""
        print("\nUpdating absence entitlements...\n")
        hours = self.generate_absence_summary()[2] * 8
        (entitlements.Entitlements(self.id_)
                     .update_hours(hours, "unallocated_to_pending"))
        print(colour("GREEN", "Absence entitlements updated successfully."))


class CancelAbsence:
    """Represent cancel Absence menu option.

    Args:
        id_ str: Employee ID that was used to log in.
    """

    def __init__(self, id_):
        self.id_ = id_
        self.absence_sheet = requests.Requests(id_)
        self.absences = self.absence_sheet.get_cancellable_absence()
        self.cancel_absence()

    def cancel_absence(self):
        """Get absence request data from a user.
        Run a while loop until no cancellable absence left.
        """
        while len(self.absences) > 0:
            self.req_id = self.get_cancel_id()
            self.confirm = self.get_confirm_cancel()
            if self.confirm == "Y":
                self.update_cancel_absence()
                for absence in self.absences:
                    if self.req_id == absence[0]:
                        self.absences.pop(self.absences.index(absence))
            else:
                print(colour("GREEN", "No Absence cancelled."))
            print("\nReturning to the beginning...")
            time.sleep(3)
            utility.clear()
        print(colour("RED", "No planned/pending absence to cancel.\n"))
        menu_or_quit(self.id_)

    def display_allocated_absences(self):
        """Display absence requests that can be cancelled by the user."""
        table = []
        for item in self.absences:
            item = item[:7]
            item.pop(1)
            item[-1] = f"{item[-1]} day(s)"
            table.append(item)
        headers = (["ID", "Start Date", "End Date",
                    "Start Time", "End Time", "Duration"])
        utility.display_table(table, headers)

    def get_cancel_id(self):
        """Ask the user to input absence request ID to cancel."""
        print("Loading data...")
        utility.clear()
        while True:
            print(self.id_ + "\'s Planned/Pending absence")
            self.display_allocated_absences()
            id_list = [int(item[0]) for item in self.absences]
            print(f"\nEnter a {colour('CYAN', 'request ID')}",
                  "from the first column to cancel.")
            print(f"({messages.to_menu()})")
            answer = input(colour("CYAN", ">>>\n")).strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(self.id_)
                break
            if answer.upper() == "QUIT":
                title.display_goodbye()
                sys.exit()
            elif validate_choice_number(answer, id_list):
                return answer

    def get_confirm_cancel(self):
        """Ask user to confirm to cancel an absence request."""
        for item in self.absences:
            if item[0] == self.req_id:
                absence_details = item
        if absence_details[4]:
            period = f"{absence_details[4]} - {absence_details[5]}"
        else:
            period = f"{absence_details[6]} day(s)"
        while True:
            print(colour("YELLOW", "Please confirm the cancellation."))
            print(f"Start date: {absence_details[2]}")
            print(f"End date: {absence_details[3]}")
            print(f"Period: {period}")
            print("\nCancel this absence?")
            answer = input(f"{messages.y_or_n()}\n").upper().strip()
            utility.clear()
            if validate_choice_letter(answer, ["Y", "N"]):
                return answer

    def update_cancel_absence(self):
        """Update absence_requests and entitlements worksheets."""
        utility.clear()
        print("Processing your request...\n")
        for item in self.absences:
            if self.req_id == item[0]:
                cancel_row = int(item[0])
        self.absence_sheet.update_cancelled(cancel_row)
        for absence in self.absences:
            if self.req_id == absence[0]:
                list_index = self.absences.index(absence)
        absence_days = self.absences[list_index][6]
        absence_hours = int(float(absence_days) * 8)
        is_approved = self.absences[list_index][8]
        entitle_sheet = entitlements.Entitlements(self.id_)
        if is_approved == "True":
            entitle_sheet.update_hours(absence_hours, "planned_to_unallocated")
        else:
            entitle_sheet.update_hours(absence_hours, "pending_to_unallocated")
        print(colour("GREEN", "Absence cancelled successfully."))


def menu_or_quit(id_):
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid option.

    Args:
        id_ str: Employee ID that was used to log in.
    Returns:
        str: The user input - menu or quit.
    """
    while True:
        print(messages.to_menu())
        answer = input(colour("CYAN", ">>>\n")).upper().strip()
        if validate_choice_letter(answer, ["MENU", "QUIT"]):
            if answer == "MENU":
                utility.clear()
                employee_main(id_)
                break
            title.display_goodbye()
            sys.exit()
