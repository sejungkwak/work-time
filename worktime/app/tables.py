"""Tables Module
"""

# Third-party Package
from tabulate import tabulate

# Custom Package
from worktime.worksheets import employees, entitlements


def display_table(table, headers=None):
    """Display a table with a solid border.

    Args:
        table list: A list of lists - The Content of the table.
                    If headers is None, all cotents display in a box.
        headers list: Names of the columns.
    """
    if headers is None:
        print(tabulate(table, tablefmt="fancy_grid"))
    else:
        print(tabulate(table, headers, tablefmt="fancy_grid"))


def display_entitlements(id_):
    """Retrieve absence entitlements from the entitlements module and display it.

    Args:
        id_ str: An employee ID.
    """
    data = entitlements.Entitlements(id_).get_entitlements()
    table = [[item for item in data]]
    headers = ["Total Hours", "Taken", "Planned", "Pending", "Unallocated"]
    display_table(table, headers)


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
        if len(table) > 1:
            print(f"\nNew requests from {fullname}")
        else:
            print(f"\nNew request from {fullname}")
        display_table(table, headers)
