"""Login_credentials Worksheet Module

This module provides functions to retrieve login credential data
from the worksheet.
"""

# Custom Package
from worktime.worksheets import auth


class Credentials:
    """Represents the login_credentials worksheet.
        Column A: employee_id
        Column B: password
    """

    def __init__(self):
        self.worksheet = auth.SHEET.worksheet("login_credentials")
        self.credentials = self.worksheet.get_all_values()[1:]

    def ids(self):
        """Returns a list of employee IDs."""
        ids = [id for id, pw in self.credentials]
        return ids
