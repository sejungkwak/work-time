"""Absence Requests Worksheet Module

This module provides functions to add and update
absence details in the worksheet.
"""

# Custom Package
from worktime.worksheets import auth
from worktime.app import utility


class Requests:
    """Represent the absence_requests worksheet.
        Column A: request_id
        Column B: employee_id
        Column C: start_date
        Column D: end_date
        Column E: start_time
        Column F: end_time
        Column G: total_days
        Column H: requested_on
        Column I: approved
        Column J: cancelled

    Args:
        id_ str: An employee ID
    """

    today = utility.GetDatetime().tday_str()

    def __init__(self, id_=None):
        self.id_ = id_
        self.worksheet = auth.SHEET.worksheet("absence_requests")
        self.requests = self.worksheet.get_all_values()[1:]
        self.req_id_col = "A"
        self.duration_col = "G"
        self.approved_col = "I"
        self.cancelled_col = "J"

    def generate_req_id(self):
        """Increment the request ID by 1.
        If there hasn't been a request, assign 1 to it.

        Returns:
            int: Request ID.
        """
        request_id = 1
        if self.requests:
            request_id = int([request[0] for request in self.requests][-1]) + 1
        return request_id

    def add_request(self, data):
        """Add new request data to the worksheet.

        Args:
            data list: A list containing request details - request ID,
            employee ID, start/end date, start/end time, total number of days,
            request date, default approved and cancelled values.
        """
        self.worksheet.append_row(data, value_input_option='RAW')

    def update_approved(self, row, action):
        """Replace False or True with "/" in a approved cell.

        Args:
            row int: The index of the target row which starts with 1.
        """
        result = "True" if action == "APPROVE" else "False"
        (self.worksheet.update(f"{self.approved_col}{row+1}",
                               f"{result}", raw=True))

    def update_cancelled(self, row):
        """Replace False with True in a cancelled cell.

        Args:
            row int: The index of the target row.
        """
        self.worksheet.update(f"{self.cancelled_col}{row+1}", "True", raw=True)

    def get_today_absence(self):
        """Check if today is the start date of planned absence.

        Returns:
            list: A list of lists containing the employee ID and duration.
        """
        today_list = []
        for request in self.requests:
            if (request[2] == self.today and request[-2] == "True" and
                    request[-1] == "False"):
                today_list.append([request[1], request[6]])
        return today_list

    def get_duration(self, row):
        """Get the total_days column(index 6) of the given row's value.

        Args:
            row int: The index of the target row.
        Returns:
            str: Total days of an absence request.
        """
        duration = self.requests[row-1][6]
        return duration

    def get_approved(self, row):
        """Get the approved column(index 8) of the given row's value.

        Args:
            row int: The index of the target row.
        Returns:
            str: Value of approved cell - True, False or /.
        """
        is_approved = self.requests[row-1][8]
        return is_approved

    def get_cancelled(self, row):
        """Get the cancelled column(index 9) of the given row's value.

        Args:
            row int: The index of the target row.
        Returns:
            str: Value of cancelled cell - True or False.
        """
        is_cancelled = self.requests[row-1][9]
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
            if (request[1] == self.id_ and (date - today).days > 0 and
                    not request[-2] == "False" and request[-1] == "False"):
                cancellable.append(request)
        return cancellable
