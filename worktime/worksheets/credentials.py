# Custom Package
from worktime.worksheets import auth


class Credentials:
    """Represents the login_credentials worksheet."""

    def __init__(self):
        self.worksheet = auth.SHEET.worksheet("login_credentials")
        self.credentials = self.worksheet.get_all_values()[1:]

    def ids(self):
        """Returns a list of employee IDs."""
        ids = [id for id, pw in self.credentials]
        return ids

    def pw(self, id):
        """Returns a matching password for the ID.

        Args:
            :id str: An employee ID
        """
        for credential in self.credentials:
            if id in credential:
                index = self.credentials.index(credential)
                pw = self.credentials[index][1]
                return pw
