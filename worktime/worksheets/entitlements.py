# Custom Package
from worktime.worksheets import auth


class Entitlements:
    """Represent the entitlements worksheet.

    Args:
        id str: An employee ID
    """

    def __init__(self, id):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("entitlements")
        self.entitlements = self.worksheet.get_all_values()[1:]

    def get_entitlements(self):
        """Retrieve an employee's entitlements in a list."""
        for entitlement in self.entitlements:
            if self.id == entitlement[0]:
                return entitlement[1:]

    def get_row(self):
        """Return the worksheet row index which is 1-based."""
        for row, entitlement in enumerate(self.entitlements):
            if self.id == entitlement[0]:
                return row + 2

    def get_hours(self, code):
        """Return the current value of target cell.

        Args:
            code str: Absence status - taken, planned, pending or unallocated.
        """
        row = self.get_row() - 2
        # ord() returns unicode code number. i.e. A = 65.
        # To get the 0-based index, it needs to be abstracted by 65.
        col = ord(self.get_col(code)) - 65
        current_hours = self.entitlements[row][col]
        return int(current_hours)

    def update_hours(self, hours, direction):
        """Add and subtract the value of hours to / from the cell
        depending on the value of argument "direction".

        Args:
            hours int: The operand - requested absence hours.
            direction str: Cell names
        """
        row = self.get_row()
        taken_col = self.get_col("taken")
        planned_col = self.get_col("planned")
        pending_col = self.get_col("pending")
        unallocated_col = self.get_col("unallocated")
        if direction == "unallocated_to_pending":
            pending_hours = self.get_hours("pending") + hours
            unallocated_hours = self.get_hours("unallocated") - hours
            self.worksheet.update(f"{pending_col}{row}:{unallocated_col}{row}",
                                  [[pending_hours, unallocated_hours]])
        elif direction == "pending_to_unallocated":
            pending_hours = self.get_hours("pending") - hours
            unallocated_hours = self.get_hours("unallocated") + hours
            self.worksheet.update(f"{pending_col}{row}:{unallocated_col}{row}",
                                  [[pending_hours, unallocated_hours]])
        elif direction == "pending_to_planned":
            pending_hours = self.get_hours("pending") - hours
            planned_hours = self.get_hours("planned") + hours
            self.worksheet.update(f"{planned_col}{row}:{pending_col}{row}",
                                  [[planned_hours, pending_hours]])
        elif direction == "unallocated_to_planned":
            pending_hours = self.get_hours("pending")
            planned_hours = self.get_hours("planned") + hours
            unallocated_hours = self.get_hours("unallocated") - hours
            self.worksheet.update(f"{planned_col}{row}:{unallocated_col}{row}",
                                  [[planned_hours, pending_hours,
                                   unallocated_hours]])
        elif direction == "planned_to_unallocated":
            pending_hours = self.get_hours("pending")
            planned_hours = self.get_hours("planned") - hours
            unallocated_hours = self.get_hours("unallocated") + hours
            self.worksheet.update(f"{planned_col}{row}:{unallocated_col}{row}",
                                  [[planned_hours, pending_hours,
                                   unallocated_hours]])
        elif direction == "unallocated_to_taken":
            taken_hours = self.get_hours("taken") + hours
            planned_hours = self.get_hours("planned")
            pending_hours = self.get_hours("pending")
            unallocated_hours = self.get_hours("unallocated") - hours
            self.worksheet.update(f"{taken_col}{row}:{unallocated_col}{row}",
                                  [[taken_hours, planned_hours,
                                   pending_hours, unallocated_hours]])

    def get_col(self, code):
        """Return the worksheet column index.

        Args:
            code str: Absence status - taken, planned, pending or unallocated.
        """
        if code == "taken":
            col = "C"
        elif code == "planned":
            col = "D"
        elif code == "pending":
            col = "E"
        else:
            col = "F"
        return col
