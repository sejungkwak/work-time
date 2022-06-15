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

    def pw(self, id_):
        """Returns a matching password for the ID.

        Args:
            :id_ str: An employee ID
        """
        for credential in self.credentials:
            if id_ in credential:
                index = self.credentials.index(credential)
                password = self.credentials[index][1]
                return password
