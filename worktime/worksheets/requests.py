# Custom Package
from worktime.worksheets import auth
from worktime.app import utility


class Requests:
    """Represent the absence_requests worksheet.

    Args:
        :id str: An employee ID
    """

    today = utility.get_current_datetime()["date"]

    def __init__(self, id=None):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("absence_requests")
        self.requests = self.worksheet.get_all_values()[1:]
        self.req_id_col = "A"
        self.duration_col = "G"
        self.approved_col = "I"
        self.cancelled_col = "J"

    def generate_req_id(self):
        """Increment the request ID by 1.
        If there hasn't been a request, assign 1 to it.
        """
        request_id = 1
        if self.requests != []:
            request_id = int([request[0] for request in self.requests][-1]) + 1
        return request_id

    def add_request(self, data):
        """Add new request data to the worksheet.

        Args:
            :data list: A list containing request details - request ID,
            employee ID, start/end date, start/end time, total number of days,
            request date, default approved and cancelled values.
        """
        self.worksheet.append_row(data, value_input_option='RAW')

    def update_approved(self, row, action):
        """Replace False or True with "/" in a approved cell.

        Args:
            :row int: The index of the target row which starts with 1.
        """
        result = "True" if action == "APPROVE" else "False"
        (self.worksheet.update(f"{self.approved_col}{row}",
                               f"{result}", raw=True))

    def update_cancelled(self, row):
        """Replace False with True in a cancelled cell.

        Args:
            :row int: The index of the target row which starts with 1.
        """
        self.worksheet.update(f"{self.cancelled_col}{row}", "True", raw=True)

    def get_today_absence(self):
        """Check if today is the start date of planned absence.

        Returns:
            list: A list of lists containing the employee ID and duration.
        """
        today_list = []
        for request in self.requests:
            if (request[2] == self.today and request[-2] == "True" and
                    not eval(request[-1])):
                today_list.append([request[1], request[6]])
        return today_list

    def get_duration(self, row):
        """Return total days of an absence request.

        Args:
            :row int: The index of the target row which starts with 1.
        """
        duration = self.worksheet.acell(f"{self.duration_col}{row}").value
        return duration

    def get_approved(self, row):
        """Return the value of an approved cell.
        Default is "/", or else "True" or "False".

        Args:
            :row int: The index of the target row which starts with 1.
        """
        is_approved = self.worksheet.acell(f"{self.approved_col}{row}").value
        return is_approved

    def get_cancelled(self, row):
        """Return the value of an approved cell.
        Default is "False".

        Args:
            :row int: The index of the target row which starts with 1.
        """
        is_cancelled = self.worksheet.acell(f"{self.cancelled_col}{row}").value
        return is_cancelled

    def get_cancellable_absence(self):
        """Retrieve data that meets the condition: start date is in the future,
        not rejected and not cancelled.

        Returns:
            list: A list of lists containing cancellable absence data.
        """
        cancellable = []
        today = utility.convert_date(self.today)
        for request in self.requests:
            date = utility.convert_date(request[2])
            if (request[1] == self.id and (date - today).days > 0 and
                    not request[-2] == "False" and request[-1] == "False"):
                cancellable.append(request)
        return cancellable

    def get_new_requests(self):
        """Retrieve data that meets the condition: start date is in the future,
        not approved or rejected, not cancelled.

        Returns:
            list: A list of lists containing new request data.
        """
        new_requests = []
        today = utility.convert_date(self.today)
        for request in self.requests:
            date = utility.convert_date(request[2])
            if ((date - today).days > 0 and
                    request[-2] == "/" and request[-1] == "False"):
                new_requests.append(request)
        return new_requests
