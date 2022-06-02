# Custom Package
from worktime.worksheets import auth


class Employees:
    """Retrieves employee data from the employees sheet.

    Args:
        :id str: Employee ID that was used to log in.
    """

    worksheet = auth.SHEET.worksheet("employees")
    id_col = "A"
    fname_col = "B"
    lname_col = "C"

    def __init__(self, id=None):
        self.id = id

    def get_fname(self):
        """Returns the employee's first name."""
        row = self.worksheet.find(self.id).row
        fname = self.worksheet.acell(f"{self.fname_col}{row}").value
        return fname
