# Custom Package
from worktime.worksheets import auth


class Employees:
    """Represents the employees worksheet.

    Args:
        :id str: An employee ID.
    """

    def __init__(self, id=None):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("employees")
        self.employees = self.worksheet.get_all_values()[1:]

    def get_fname(self):
        """Returns the employee's first name."""
        for employee in self.employees:
            if employee[0] == self.id:
                fname = employee[1]
                return fname

    def get_lname(self):
        """Returns the employee's last name."""
        for employee in self.employees:
            if employee[0] == self.id:
                lname = employee[2]
                return lname
