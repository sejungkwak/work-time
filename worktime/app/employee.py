# Built-in Modules
import sys
import time

# Custom Packages
from worktime.worksheets import clockings, entitlements, requests
from worktime.app import menu, messages, tables, title, utility, validations


def employee_main(id):
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
        id str: Employee ID that was used to log in.
    """
    while True:
        menu.employee_menu()
        choice = input(f"{utility.cyan('>>>')}\n").strip()
        if validations.validate_choice_number(choice, range(1, 8)):
            break

    if choice == "1":
        clock_in(id)
    elif choice == "2":
        clock_out(id)
    elif choice == "3":
        get_attendance_date(id)
    elif choice == "4":
        display_entitlements(id)
    elif choice == "5":
        BookAbsence(id).book_absence()
    elif choice == "6":
        CancelAbsence(id).cancel_absence()
    else:
        title.title_end()
        sys.exit()


def clock_in(id):
    """Run when the user chooses the clock in option.
    Send the clock in data to the worksheet.

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    today = utility.GetDatetime().tday_str()
    clock_in_at = utility.GetDatetime().now_time_str()
    clock_sheet = clockings.Clockings(id)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(f"{utility.red(id + ' already clocked out at')}",
                  f"{utility.red(clocked_out_at + '.')}")
            print(f"{utility.red('To update the clock in time,')}",
                  f"{utility.red('please contact your manager.')}")
        else:
            clocked_in_at = clocking["start_time"]
            print(f"{utility.yellow(id + ' already clocked in for today at')}",
                  f"{utility.yellow(clocked_in_at + '.')}")
            print("Overwrite it?")
            answer = check_for_overwrite()
            utility.clear()
            if answer == "Y":
                print("Updating today's clock in time...")
                clock_sheet.update_clock_in(today, clock_in_at)
                print(f"{utility.green('Clock in time has been updated to')}",
                      f"{utility.green(clock_in_at + '.')}")
            else:
                print(f"{utility.green('No changes were made.')}")
    else:
        print("Submitting today's clock in time...")
        data = [id, today, clock_in_at]
        clock_sheet.add_clocking(data)
        print(f"{utility.green('Successfully clocked in at')}",
              f"{utility.green(clock_in_at + '.')}")
    menu_or_quit(id)


def check_for_overwrite():
    """Run a while loop until the user inputs a valid value.

    Returns:
        str: The user input - Y or N
    """
    while True:
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            return answer


def clock_out(id):
    """Check if there is clocking data for today already and update worksheet.

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    today = utility.GetDatetime().tday_str()
    clock_out_at = utility.GetDatetime().now_time_str()
    clock_sheet = clockings.Clockings(id)
    clocking = clock_sheet.get_one_clocking()
    if clocking:
        if clocking["end_time"]:
            clocked_out_at = clocking["end_time"]
            print(utility.red(id + ' already clocked out at ' +
                  clocked_out_at + '.'))
            print("Please contact your manager",
                  "to update your clock out time.")
        else:
            clock_sheet.update_clock_out(today, clock_out_at)
            print(utility.green("Successfully clocked out at"),
                  utility.green(clock_out_at + "."))
    else:
        data = [id, today, "", clock_out_at]
        clock_sheet.add_clocking(data)
        print(f"{utility.red('No clock in data for today.')}")
        print("Please contact your manager",
              "to add your clock in time.")
        print(utility.green("Successfully clocked out at"),
              utility.green(clock_out_at + "."))
    menu_or_quit(id)


def get_attendance_date(id):
    """Display this week's clock cards and then ask if the user wants
    to review other weeks. Run a while loop until they input a valid answer.

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    if not display_attendance(id):
        print("No clocking data found for this week.")

    while True:
        print(f"Enter a {utility.cyan('date')} to review another week.")
        print(messages.date_format())
        print(f"({messages.to_menu()})")
        answer = input(f"{utility.cyan('>>>')}\n").strip()
        utility.clear()
        if answer.upper() == "MENU":
            employee_main(id)
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_date(answer):
            utility.clear()
            display_attendance(id, answer)


def display_attendance(id, date=None):
    """Check if there is any clock in/out data, and then display the result.

    Args:
        date str: A DD/MM/YYYY formatted date. Today if none.
    Returns:
        bool: True if there are clock cards.
    """
    utility.clear()
    print("Getting clocking data...")
    today = utility.GetDatetime().tday_str()
    date = today if date is None else date
    data = False
    headers = ["ID", "Date", "Clock In", "Clock Out"]
    clock_sheet = clockings.Clockings(id)
    table = clock_sheet.get_week_clockings(date)
    if table:
        data = True
        utility.clear()
        print("Clock cards display from Monday to Sunday.")
        tables.display_table(table, headers)
    else:
        utility.clear()
        print("No clocking data found.")
    return data


def display_entitlements(id):
    """Display absence entitlements for the logged in employee

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    this_year = utility.GetDatetime().now_year()
    print(f"\nAbsence entitlements for {this_year}.")
    tables.display_entitlements(id)
    menu_or_quit(id)


class BookAbsence:
    """Represent Book Absence menu option.

    Args:
        id str: Employee ID that was used to log in.
    """
    def __init__(self, id):
        self.id = id
        self.unallocated = entitlements.Entitlements(id).get_entitlements()[-1]
        self.avail_hours = int(self.unallocated)

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

            if self.duration == 1:
                self.start_time = "9:30"
                self.end_time = "13:30"
                self.period = f"{self.start_time} - {self.end_time}"
                self.hours = 4
            elif self.duration == 2:
                self.start_time = "13:30"
                self.end_time = "17:30"
                self.period = f"{self.start_time} - {self.end_time}"
                self.hours = 4
            elif self.duration == 3:
                self.start_time = ""
                self.end_time = ""
                self.period = "1 workday"
                self.hours = 8
            else:
                self.start_time = ""
                self.end_time = ""
                self.days = (utility.get_num_of_weekdays(self.start_date,
                                                         self.end_date))
                self.period = f"{self.days} workdays"
                self.hours = self.days * 8

            self.confirm = self.get_confirm_request()
            if self.confirm == "Y":
                self.add_absence_request()
                self.add_pending_hours()
                self.avail_hours -= self.hours
            else:
                print(utility.green("No requests were submitted."))
            print("\nReturning to the beginning...")
            time.sleep(3)
            utility.clear()
        else:
            self.display_avail_hours()
            menu_or_quit(self.id)

    def display_avail_hours(self):
        """Display the employee's available paid time off hours."""
        utility.clear()
        if self.avail_hours == 0:
            print(utility.red("Insufficient paid time off available"),
                  utility.red("to book absence.\n"))
        else:
            print(f"{self.avail_hours} hours available to book absence.\n")

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
            answer = input(f"{utility.cyan('>>>')}\n").strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(self.id)
                break
            elif answer.upper() == "QUIT":
                title.title_end()
                sys.exit()
            elif validations.validate_choice_number(answer, range(1, 5)):
                if ((answer == "4" and self.avail_hours < 16) or
                        (answer == "3" and self.avail_hours < 8)):
                    print(utility.red("Insufficient paid time off available"),
                          utility.red("to complete the request."))
                    print("Select a different option or contact your manager.")
                else:
                    return int(answer)

    def get_start_date(self):
        """Ask user to input the absence (start) date.

        Return:
            str: User input if successful.
        """
        utility.clear()
        while True:
            if self.duration in range(1, 4):
                print(f"Please enter the {utility.cyan('absence date')}.")
            else:
                print(f"Please enter the {utility.cyan('start date')}",
                      "for the absence duration.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(f"{utility.cyan('>>>')}\n").strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(self.id)
                break
            elif answer.upper() == "QUIT":
                title.title_end()
                sys.exit()
            elif validations.validate_date(answer):
                request_date = utility.convert_date(answer)
                today = utility.GetDatetime().tday()
                request_year = request_date.year
                this_year = utility.GetDatetime().now_year()
                if (request_date - today).days <= 0:
                    print(f"\n{utility.red('Please note holidays must be')}",
                          f"{utility.red('booked in advance.')}")
                    print(f"{utility.red('If you would like to submit')}",
                          f"{utility.red('absence in the past,')}",
                          f"{utility.red('please contact your manager.')}")
                elif request_year != this_year:
                    print(messages.invalid_year())
                elif request_date.weekday() > 4:
                    print(utility.red("No absence requests required"),
                          utility.red("for weekends."))
                else:
                    return answer

    def get_end_date(self):
        """Ask user to input absence end date if they are booking 2+ days.

        Return:
            str: User input if successful.
        """
        utility.clear()
        while True:
            print(f"Please enter the {utility.cyan('last date')}",
                  "for the absence duration.")
            print(messages.date_format())
            print(f"({messages.to_menu()})")
            answer = input(f"{utility.cyan('>>>')}\n").strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(self.id)
                break
            elif answer.upper() == "QUIT":
                title.title_end()
                sys.exit()
            elif (validations.validate_date(answer) and
                    (validations.validate_days(self.start_date, answer,
                                               self.avail_hours))):
                return answer

    def get_confirm_request(self):
        """Display absence request summary and ask user to confirm to submit.

        Returns:
            str: User input - Y or N.
        """
        while True:
            print(f"{utility.yellow('Please confirm your request.')}")
            print(f"Start date: {self.start_date}")
            print(f"End date: {self.end_date}")
            print(f"Period: {self.period}")
            if self.duration == 4:
                print("Please note that weekends are not included.")
            print("\nSubmit this request?")
            answer = input(f"{messages.y_or_n()}\n").upper().strip()
            utility.clear()
            if validations.validate_choice_letter(answer, ["Y", "N"]):
                return answer

    def add_absence_request(self):
        """Update the absence_requests worksheet."""
        print("Submitting your absence request...\n")
        self.request_sheet = requests.Requests()
        self.req_id = self.request_sheet.generate_req_id()
        self.today = utility.GetDatetime().tday_str()
        data = ([self.req_id, self.id, self.start_date, self.end_date,
                 self.start_time, self.end_time,
                 self.hours / 8, self.today, "/", "False"])
        self.request_sheet.add_request(data)
        print(f"{utility.green('Absence request submitted successfully.')}")
        time.sleep(3)
        utility.clear()

    def add_pending_hours(self):
        """Update the entitlements worksheet."""
        print("Updating absence entitlements...\n")
        (entitlements.Entitlements(self.id)
                     .update_hours(self.hours, "unallocated_to_pending"))
        print(f"{utility.green('Absence entitlements updated successfully.')}")


class CancelAbsence:
    """Represent cancel Absence menu option.

    Args:
        id str: Employee ID that was used to log in.
    """

    def __init__(self, id):
        self.id = id
        self.absence_sheet = requests.Requests(id)
        self.absences = self.absence_sheet.get_cancellable_absence()

    def cancel_absence(self):
        """Get absence request data from a user.
        Run a while loop until no cancellable absence left.
        """
        utility.clear()
        while len(self.absences) > 0:
            self.req_id = self.get_cancel_id()
            self.confirm = self.get_confirm_cancel()
            if self.confirm == "Y":
                self.update_cancel_absence()
                for absence in self.absences:
                    if self.req_id == absence[0]:
                        self.absences.pop(self.absences.index(absence))
            else:
                print(utility.green("No Absence cancelled.\n"))
            print("Returning to the beginning...")
            time.sleep(3)
            utility.clear()
        else:
            print(utility.red("No planned/pending absence to cancel."))
            menu_or_quit(self.id)

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
        tables.display_table(table, headers)

    def get_cancel_id(self):
        """Ask the user to input absence request ID to cancel."""
        print("Loading data...")
        utility.clear()
        while True:
            self.display_allocated_absences()
            id_list = [int(item[0]) for item in self.absences]
            print(f"\nEnter a {utility.cyan('request ID')}",
                  "from the first column to cancel.")
            print(f"({messages.to_menu()})")
            answer = input(f"{utility.cyan('>>>')}\n").strip()
            utility.clear()
            if answer.upper() == "MENU":
                employee_main(id)
                break
            elif answer.upper() == "QUIT":
                title.title_end()
                sys.exit()
            elif validations.validate_choice_number(answer, id_list):
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
            print(f"{utility.yellow('Please confirm the cancellation.')}")
            print(f"Start date: {absence_details[2]}")
            print(f"End date: {absence_details[3]}")
            print(f"Period: {period}")
            print("\nCanel this absence?")
            answer = input(f"{messages.y_or_n()}\n").upper().strip()
            utility.clear()
            if validations.validate_choice_letter(answer, ["Y", "N"]):
                return answer

    def update_cancel_absence(self):
        """Update absence_requests and entitlements worksheets."""
        utility.clear()
        print("\nProcessing your request...\n")
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
        entitle_sheet = entitlements.Entitlements(self.id)
        if is_approved == "True":
            entitle_sheet.update_hours(absence_hours, "planned_to_unallocated")
        else:
            entitle_sheet.update_hours(absence_hours, "pending_to_unallocated")
        print(f"{utility.green('Absence cancelled successfully.')}\n")


def menu_or_quit(id):
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid option.

    Args:
        id str: Employee ID that was used to log in.
    Returns:
        str: The user input - menu or quit.
    """
    while True:
        print(messages.to_menu())
        answer = input(f"{utility.cyan('>>>')}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["MENU", "QUIT"]):
            if answer == "MENU":
                utility.clear()
                employee_main(id)
                break
            else:
                title.title_end()
                sys.exit()
