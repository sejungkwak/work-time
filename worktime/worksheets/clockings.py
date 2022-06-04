# Custom Package
from worktime.worksheets import auth
from worktime.app import utility


class Clockings:
    """Represent the clockings worksheet.

    Args:
        :id str: An employee ID
    """

    today = utility.get_current_datetime()["date"]

    def __init__(self, id=None):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("clockings")
        self.clockings = self.worksheet.get_all_values()[1:]
        self.clock_in_col = "C"
        self.clock_out_col = "D"

    def add_clocking(self, data):
        """Add clocking data to the worksheet."""
        self.worksheet.append_row(data)

    def update_clock_in(self, time):
        """Replace an existing clock in data with a new one."""
        row = self.get_one_clocking()["row"]
        self.worksheet.update(f"{self.clock_in_col}{row}", time)

    def update_clock_out(self, time):
        """Replace an existing clock out data with a new one."""
        row = self.get_one_clocking()["row"]
        self.worksheet.update(f"{self.clock_out_col}{row}", time)

    def get_one_clocking(self, target_date=None):
        """Return clocking data with row number in a dictionary."""
        target_date = self.today if target_date is None else target_date
        for row, clocking in enumerate(self.clockings, start=2):
            id, date, clock_in, clock_out = clocking
            if id == self.id and date == target_date:
                return ({"row": row, "id": id, "date": date,
                        "start_time": clock_in, "end_time": clock_out})

    def get_week_clockings(self, target_date=None):
        """Return a week's clocking data in a list of lists"""
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
