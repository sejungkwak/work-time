"""Clockings Worksheet Module

This module provides functions to add and update
clock in/out time in the worksheet.
"""

# Custom Package
from worktime.worksheets import auth
from worktime.app import utility


class Clockings:
    """Represent the clockings worksheet:
        Column A: employee_id
        Column B: date
        Column C: clocked_in_at
        Column D: clocked_out_at

    Args:
        ee_id str: An employee ID
    """

    today = utility.GetDatetime().tday_str()

    def __init__(self, ee_id=None):
        self.ee_id = ee_id
        self.worksheet = auth.SHEET.worksheet("clockings")
        self.clockings = self.worksheet.get_all_values()[1:]
        self.clock_in_col = "C"
        self.clock_out_col = "D"

    def add_clocking(self, data):
        """Add clocking data to the worksheet.

        Args:
            data list: Contains Employee ID, Date, Clock in, Clock out
        """
        self.worksheet.append_row(data)

    def update_clock_in(self, date_, time_):
        """Replace an existing clock in time with a new one.

        Args:
            date_ str: A DD/MM/YYYY format date.
            time_ str: A HH:MM:SS format time.
        """
        row = self.get_one_clocking(date_)["row"]
        self.worksheet.update(f"{self.clock_in_col}{row}", time_)

    def update_clock_out(self, date_, time_):
        """Replace an existing clock out time with a new one.

        Args:
            date_ str: A DD/MM/YYYY format date.
            time_ str: A HH:MM:SS format time.
        """
        row = self.get_one_clocking(date_)["row"]
        self.worksheet.update(f"{self.clock_out_col}{row}", time_)

    def get_one_clocking(self, target_date=None):
        """Iterate through the sheet to find row values that match the ID and date.

        Args:
            target_date str: A DD/MM/YYYY format date. Today if none.
        Returns:
            dict: Clocking data with a sheet's row number.
        """
        target_date = self.today if target_date is None else target_date
        for row, clocking in enumerate(self.clockings, start=2):
            ee_id, date, clock_in, clock_out = clocking
            if ee_id == self.ee_id and date == target_date:
                return ({"row": row, "id": ee_id, "date": date,
                        "start_time": clock_in, "end_time": clock_out})
