# Custom Package
from worktime.worksheets import auth


class Entitlements:
    """Represent the entitlements worksheet.

    Args:
        :id str: An employee ID
    """

    def __init__(self, id):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("entitlements")
        self.entitlements = self.worksheet.get_all_values()[1:]

    def get_entitlements(self):
        """Retrive an employee's entitlements in a list."""
        for entitlement in self.entitlements:
            if self.id == entitlement[0]:
                return entitlement[1:]

    def get_row(self):
        """Return the worksheet row index which is 1-based."""
        for entitlement in self.entitlements:
            if self.id == entitlement[0]:
                row = self.entitlements.index(entitlement) + 2
                return row

    def get_hours(self, code):
        """Return the current value of target cell.

        Args:
            :code str: Absence status - taken, planned, pending or unallocated.
        """
        row = self.get_row() - 2
        # ord() returns unicode code number. i.e. A = 65.
        # To get the 0-based index, it needs to be abstracted by 65.
        col = ord(self.get_col(code)) - 65
        current_hours = self.entitlements[row][col]
        return int(current_hours)

    def update_hours(self, code, hours, math):
        """Update hours on the worksheet.

        Args:
            :code str: Absence status - taken, planned, pending or unallocated.
            :hours int: The operand.
            :math str: Type of mathematical operations - add or subtract.
        """
        row = self.get_row()
        col = self.get_col(code)
        current = self.get_hours(code)
        new = current + hours if math == "add" else current - hours
        self.worksheet.update(f"{col}{row}", new)

    def get_col(self, code):
        """Return the worksheet column index.

        Args:
            :code str: Absence status - taken, planned, pending or unallocated.
        """
        col = ""
        if code == "taken":
            col = "C"
        elif code == "planned":
            col = "D"
        elif code == "pending":
            col = "E"
        else:
            col = "F"
        return col
