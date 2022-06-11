# Custom Package
from worktime.worksheets import auth
from worktime.app import utility


class Clockings:
    """Represent the clockings worksheet.

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

    def get_week_clockings(self, target_date=None):
        """Iterate through the sheet to find week's values that match the date.

        Args:
            target_date str: A DD/MM/YYYY format date. Today if none.
        Returns:
            list: A list of lists containing a week's clocking data.
        """
        target_date = self.today if target_date is None else target_date
        target_date = utility.convert_date(target_date)
        dates = utility.get_week(target_date, "week")
        result = []
        for date in dates:
            if self.get_one_clocking(date) is not None:
                lists = self.get_one_clocking(date)
                lists.pop("row")
                result.append([values for keys, values in lists.items()])
        return result

    def get_one_all_employee(self, target_date):
        """Iterate through the sheet to find row values that match the date
        for all employees.

        Args:
            target_date str: A DD/MM/YYYY format date.
        Returns:
            list: A list of lists containing all employees' clocking
                  data for a day.
        """
        result = []
        for clocking in self.clockings:
            ee_id, date, clock_in, clock_out = clocking
            if date == target_date:
                result.append(clocking)
        return result
