# Custom Package
from worktime.worksheets import auth


class Employees:
    """Represents the employees worksheet.

    Args:
        :id str: Employee ID that was used to log in.
    """

    def __init__(self, id=None):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("employees")
        self.id_col = "A"
        self.fname_col = "B"
        self.lname_col = "C"

    def get_fname(self):
        """Returns the employee's first name."""
        row = self.worksheet.find(self.id).row
        fname = self.worksheet.acell(f"{self.fname_col}{row}").value
        return fname
