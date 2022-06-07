# Third-party Package
from tabulate import tabulate

# Custom Package
from worktime.worksheets import clockings, employees, entitlements, requests


def display_table(headers, table):
    """Display a table with a solid border.

    Args:
        headers list: Names of the columns.
        table list: A list of lists - The Content of the table.
    """
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def display_allocated_absences(id):
    """Display absence requests that can be cancelled by the user.

    Args:
        id str: An employee ID.
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
        id str: An employee ID.
    """
    data = entitlements.Entitlements(id).get_entitlements()
    table = [[item for item in data]]
    headers = ["Total Hours", "Taken", "Planned", "Pending", "Unallocated"]
    display_table(headers, table)


def display_new_requests(req_list):
    """Display new absence requests grouped by employee ID.

    Args:
        req_list list: A list of lists of lists containing new requests.
    """
    fullname = ""
    headers = (["ID", "Start Date", "End Date",
                "Start Time", "End Time", "Duration"])
    for request in req_list:
        table = []
        for item in request:
            item = item[:7]
            employee_id = item.pop(1)
            fullname = employees.Employees(employee_id).get_fullname()
            item[-1] = f"{item[-1]} Day(s)"
            table.append(item)
        print(f"New request(s) from {fullname}")
        display_table(headers, table)
