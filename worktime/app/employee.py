# Built-in Modules
import sys
import time

# Custom Packages
from worktime.worksheets import clockings, entitlements, requests
from worktime.app import menu, messages, tables, title, utility, validations


def employee_main(id):
    """Request a number between 1 and 7, the numbered options.
    Run a while loop until the user inputs a valid number.

    Args:
        id str: Employee ID that was used to log in.
    """
    while True:
        menu.employee_menu()
        choice = input(f"\n{messages.enter_number()}\n").strip()
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
        check_avail_hours(id)
    elif choice == "6":
        check_cancellable(id)
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
    now = utility.get_current_datetime()
    today = now["date"]
    clock_in_at = now["time"]
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
            print(f"{utility.yellow('Overwrite it?')}")
            answer = check_for_overwrite()
            utility.clear()
            if answer == "Y":
                print("Updating today's clock in time...")
                clock_sheet.update_clock_in(clock_in_at)
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
    menu_quit = menu_or_quit()
    if menu_quit == "MENU":
        utility.clear()
        employee_main(id)
    else:
        title.title_end()
        sys.exit()


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
    now = utility.get_current_datetime()
    today = now["date"]
    clock_out_at = now["time"]
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
            clock_sheet.update_clock_out(clock_out_at)
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
    menu_quit = menu_or_quit()
    if menu_quit == "MENU":
        utility.clear()
        employee_main(id)
    else:
        title.title_end()
        sys.exit()


def get_attendance_date(id):
    """Display this week's clock cards and then ask if the user wants
    to review other weeks. Run a while loop until they input a valid answer.

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    if not display_attendance(id):
        print("There is no clocking data for this week.")

    while True:
        print("\nEnter a date to review another week.")
        print(messages.date_format())
        print(messages.to_menu())
        answer = input(f"{messages.enter_date()}\n").strip()
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
    today = utility.get_current_datetime()["date"]
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
        print("There is no clocking data.")
    return data


def display_entitlements(id):
    """Display absence entitlements for the logged in employee

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    this_year = utility.get_current_datetime()["year"]
    print(f"\nAbsence entitlements for {this_year}.")
    tables.display_entitlements(id)
    menu_quit = menu_or_quit()
    if menu_quit == "MENU":
        utility.clear()
        employee_main(id)
    else:
        title.title_end()
        sys.exit()


def check_avail_hours(id):
    """Check if the employee has available paid time off hours left.

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    unallocated = entitlements.Entitlements(id).get_entitlements()[-1]

    if unallocated == "0":
        print(utility.red("Insufficient paid time off available."))
    else:
        print(f"{unallocated} hours available to book absence.\n")
        get_absence_duration(id)


def get_absence_duration(id):
    """Ask user to choose an option for the absence duration.

    Args:
        id str: Employee ID that was used to log in.
    """
    unallocated = entitlements.Entitlements(id).get_entitlements()[-1]
    while True:
        menu.absence_period_menu()
        print(f"\n{messages.to_menu()}")
        answer = input(f"\n{messages.enter_number()}\n").strip()
        if answer.upper() == "MENU":
            utility.clear()
            employee_main(id)
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(answer, range(1, 5)):
            if ((answer == "4" and float(unallocated) < 16) or
                    (answer == "3" and float(unallocated) < 8)):
                print(utility.red("Insufficient paid time off available"),
                      utility.red("to complete the request."))
                print("Select a different option or contact your manager.")
            else:
                get_absence_start_date(id, answer)
                break


def get_absence_start_date(id, duration):
    """Ask user to input the absence (start) date.

    Args:
        id str: Employee ID that was used to log in.
        duration str: Absence duration.
            1. morning, 2. afternoon, 3. full day, 4. 2+ days
    """
    while True:
        utility.clear()
        if int(duration) in range(1, 4):
            print("\nPlease enter your absence date.")
        else:
            print("\nPlease enter the start date for your absence duration.")
        print(messages.date_format())
        print(messages.to_menu())
        answer = input(f"{messages.enter_date()}\n").strip()
        if answer.upper() == "MENU":
            utility.clear()
            employee_main(id)
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        else:
            request_date = validations.validate_date(answer)
            today = utility.get_today()
            request_year = request_date.year
            this_year = int(utility.get_current_datetime()["year"])
            if (request_date - today).days <= 0:
                print(f"\n{utility.red('Please note holidays must be')}",
                      f"{utility.red('booked in advance.')}")
                print(f"{utility.red('If you would like to submit')}",
                      f"{utility.red('absence in the past,')}",
                      f"{utility.red('please contact your manager.')}")
            elif request_year != this_year:
                print(messages.invalid_year())
            else:
                if duration == "4":
                    get_absence_end_date(id, answer)
                    break
                else:
                    get_confirm_request(id, answer, answer, duration)
                    break


def get_absence_end_date(id, start_date):
    """Ask user to input absence end date if they are booking 2+ days.

    Args:
        id str: Employee ID that was used to log in.
        start_date str: The absence start date.
    """
    unallocated = entitlements.Entitlements(id).get_entitlements()[-1]
    while True:
        print("\nPlease enter the last day for your absence duration.")
        print(messages.date_format())
        print(messages.to_menu())
        answer = input(f"{messages.enter_date()}\n").strip()
        if answer.upper() == "MENU":
            utility.clear()
            employee_main(id)
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif (validations.validate_date(answer) and
              validations.validate_days(start_date, answer, unallocated)):
            get_confirm_request(id, start_date, answer, "4")
            break


def get_confirm_request(id, start_date, end_date, duration):
    """Display absence request summary and ask user to confirm to submit.

    Args:
        id str: Employee ID that was used to log in.
        start_date str: The absence start date - DD/MM/YYYY.
        end_date str: The absence end date - DD/MM/YYYY.
        duration str: Absence duration.
            1. morning, 2. afternoon, 3. full day, 4. 2+ days
    """
    if duration == "1":
        period = "9:30 - 13:30"
        hours = 4
    elif duration == "2":
        period = "13:30 - 17:30"
        hours = 4
    elif duration == "3":
        period = "1 day"
        hours = 8
    else:
        period = utility.get_num_of_weekdays(start_date, end_date)
        hours = period * 8
        period = f"{period} days"
    while True:
        utility.clear()
        print(f"{utility.yellow('Please confirm your request.')}")
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")
        print(f"Period: {period}")
        if duration == "4":
            print("Please note that the weekends are not included.")
        print("\nSubmit your request?")
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            if answer == "Y":
                add_absence_request(id, start_date, end_date, duration)
                add_pending_hours(id, hours)
                break
            else:
                print(utility.green("No requests were submitted."))
                print("Returning to the menu...")
                time.sleep(2)
                utility.clear()
                employee_main(id)
                break


def add_absence_request(id, start_date, end_date, duration):
    """Update the absence_requests worksheet.

    Args:
        id str: Employee ID that was used to log in.
        start_date str: The absence start date.
        end_date str: The absence end date.
        duration str: Absence duration.
            1. morning, 2. afternoon, 3. full day, 4. 2+ days
    """
    print("\nSubmitting your absence request...")
    request_id = requests.Requests().generate_req_id()
    today = utility.get_current_datetime()["date"]
    data = [request_id, id, start_date, today, "/", "False"]
    if duration == "1":
        data[3:3] = [start_date, "9:30", "13:30", "0.5"]
    elif duration == "2":
        data[3:3] = [start_date, "13:30", "17:30", "0.5"]
    elif duration == "3":
        data[3:3] = [start_date, "", "", "1"]
    else:
        days = str(utility.get_num_of_weekdays(start_date, end_date))
        data[3:3] = [end_date, "", "", days]
    requests.Requests().add_request(data)
    print(f"\n{utility.green('Absence request submitted successfully.')}")


def add_pending_hours(id, hours):
    """Update pending value on the entitlements worksheet.

    Args:
        id str: Employee ID that was used to log in.
        hours int: The number of requested absence hours.
    """
    print("\nUpdating absence entitlements...")
    time.sleep(1)
    entitle_sheet = entitlements.Entitlements(id)
    entitle_sheet.update_hours(hours, "unallocated_to_pending")
    print(f"\n{utility.green('Absence entitlements updated successfully.')}\n")
    menu_quit = menu_or_quit()
    if menu_quit == "MENU":
        utility.clear()
        employee_main(id)
    else:
        title.title_end()
        sys.exit()


def check_cancellable(id):
    """Check if the user has planned/pending absence.

    Args:
        id str: Employee ID that was used to log in.
    """
    utility.clear()
    entitle_sheet = entitlements.Entitlements(id)
    planned = entitle_sheet.get_hours("planned")
    pending = entitle_sheet.get_hours("pending")
    if planned == pending == 0:
        print(utility.red("No planned/pending absence to cancel."))
        menu_quit = menu_or_quit()
        if menu_quit == "MENU":
            utility.clear()
            employee_main(id)
        else:
            title.title_end()
            sys.exit()
    else:
        get_cancel_number(id)


def get_cancel_number(id):
    """Ask the user to input absence request ID to cancel.

    Args:
        id str: Employee ID that was used to log in.
    """
    print("Loading data...")
    allocated_absences = requests.Requests(id).get_cancellable_absence()
    utility.clear()
    display_allocated_absences(allocated_absences)
    while True:
        id_list = [int(item[0]) for item in allocated_absences]
        print(messages.to_menu())
        answer = input(f"{messages.enter_req_id()}\n").strip()
        if answer.upper() == "MENU":
            utility.clear()
            employee_main(id)
            break
        elif answer.upper() == "QUIT":
            title.title_end()
            sys.exit()
        elif validations.validate_choice_number(answer, id_list):
            get_confirm_cancel(id, answer, allocated_absences)


def display_allocated_absences(data):
    """Display absence requests that can be cancelled by the user.

    Args:
        data list: A list of lists containing absence requests.
    """
    table = []
    for item in data:
        item = item[:7]
        item.pop(1)
        item[-1] = f"{item[-1]} day(s)"
        table.append(item)
    headers = (["ID", "Start Date", "End Date",
                "Start Time", "End Time", "Duration"])
    tables.display_table(table, headers)


def get_confirm_cancel(id, request_id, data):
    """Ask user to confirm to cancel an absence request.

    Args:
        id str: Employee ID that was used to log in.
        request_id str: Absence request ID.
        data list: A list of lists containing absence requests.
    """
    for item in data:
        if item[0] == request_id:
            details = item
    if details[4]:
        period = f"{details[4]} - {details[5]}"
    else:
        period = f"{details[6]} day(s)"
    while True:
        utility.clear()
        print(f"{utility.yellow('Please confirm cancellation.')}")
        print(f"Start date: {details[2]}")
        print(f"End date: {details[3]}")
        print(f"Period: {period}")
        print("\nCanel this absence?")
        answer = input(f"{messages.y_or_n()}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["Y", "N"]):
            if answer == "Y":
                update_cancel_absence(id, details)
                break
            if answer == "N":
                utility.clear()
                print(utility.green("No absences were cancelled."))
                break
    time.sleep(2)
    if (answer == "Y" and len(data) > 1) or (answer == "N" and len(data) > 0):
        print("Returning to the cancellation menu...")
        time.sleep(2)
        get_cancel_number(id)
    else:
        menu_quit = menu_or_quit()
        if menu_quit == "MENU":
            utility.clear()
            employee_main(id)
        else:
            title.title_end()
            sys.exit()


def update_cancel_absence(id, request):
    """Update absence_requests and entitlements worksheets.

    Args:
        id str: Employee ID that was used to log in.
        request list: Absence to cancel.
    """
    utility.clear()
    print("\nProcessing your request...")
    row_index = int(request[0])
    requests.Requests().update_cancelled(row_index)
    absence_days = request[6]
    absence_hours = int(float(absence_days) * 8)
    is_approved = request[8]
    entitle_sheet = entitlements.Entitlements(id)
    if is_approved == "True":
        entitle_sheet.update_hours(absence_hours, "planned_to_unallocated")
    else:
        entitle_sheet.update_hours(absence_hours, "pending_to_unallocated")
    utility.clear()
    print(f"{utility.green('Absence cancelled successfully.')}\n")


def menu_or_quit():
    """Ask the user if they want to go back to the menu or quit.
    Run a while loop until the user inputs a valid option.

    Returns:
        str: The user input - menu or quit.
    """
    while True:
        print(messages.to_menu())
        answer = input(f"\n{messages.enter_menu()}\n").upper().strip()
        if validations.validate_choice_letter(answer, ["MENU", "QUIT"]):
            return answer
