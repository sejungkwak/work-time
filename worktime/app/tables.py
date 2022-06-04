# Third-party Package
from tabulate import tabulate

# Custom Package
from worktime.worksheets import clockings, entitlements, requests


def display_table(headers, table):
    """Display a table with a solid border.

    Args:
        :headers list: Names of the columns.
        :table list: A list of lists - The Content of the table.
    """
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def display_clock_card(id, date=None):
    """Retrieve clock in/out data from the clockings module and display it.

    Args:
        :id str: An employee ID.
    """
    if date is None:
        table = clockings.Clockings(id).get_week_clockings()
    else:
        table = clockings.Clockings(id).get_week_clockings(date)
    headers = ["ID", "Date", "Clock In", "Clock Out"]
    display_table(headers, table)


def display_allocated_absences(id):
    """Display absence requests that can be cancelled by the user.

    Args:
        :id str: An employee ID.
    """
    lists = requests.Requests(id).get_cancellable_absence()
    table = []
    for list in lists:
        list = list[:7]
        list.pop(1)
        list[-1] = f"{list[-1]} Day(s)"
        table.append(list)
    headers = (["ID", "Start Date", "End Date",
                "Start Time", "End Time", "Duration"])
    display_table(headers, table)


def display_entitlements(id):
    """Retrieve absence entitlements from the entitlements module and display it.

    Args:
        :id str: An employee ID.
    """
    data = entitlements.Entitlements(id).get_entitlements()
    table = [[item for item in data]]
    headers = ["Total Hours", "Taken", "Planned", "Pending", "Unallocated"]
    display_table(headers, table)
