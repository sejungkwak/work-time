# Custom Package
from worktime.worksheets import auth
from worktime.app import utility


class Clockings:
    """Represent the clockings worksheet.

    Args:
        :id str: An employee ID
    """

    def __init__(self, id=None):
        self.id = id
        self.worksheet = auth.SHEET.worksheet("clockings")
        self.clockings = self.worksheet.get_all_values()
        self.clock_in_col = "C"
        self.clock_out_col = "D"
        self.today = utility.get_datetime()["date"]

    def get_one_clocking(self, target_date=None):
        """Return clocking data with row number in a dictionary."""
        if target_date is None:
            target_date = self.today
        for row, clocking in enumerate(self.clockings, start=1):
            id, date, clock_in, clock_out = clocking
            if id == self.id and date == target_date:
                return ({"row": row, "id": id, "date": date,
                        "start_time": clock_in, "out_time": clock_out})

    def add_clocking(self, data):
        """Add clocking data to the worksheet."""
        self.worksheet.append_row(data)

    def update_clock_in(self, time):
        """Replace an existing clock in data with a new one."""
        row = self.get_today_clocking()["row"]
        self.worksheet.update(f"{self.clock_in_col}{row}", time)

    def update_clock_out(self, time):
        """Replace an existing clock out data with a new one."""
        row = self.get_today_clocking()["row"]
        self.worksheet.update(f"{self.clock_out_col}{row}", time)

    def get_week_clockings(self, date=None):
        """Return a week's clocking data in a list of lists"""
        if date is None:
            date = self.today
        datelist = date.split("/")
        year = int(datelist[2])
        month = int(datelist[1])
        day = int(datelist[0])
        weekdays = utility.get_week(year, month, day)
        result = []
        for weekday in weekdays:
            if self.get_one_clocking(weekday) is not None:
                for keys, values in self.get_one_clocking(weekday).items():
                    result.append([values])
        return result
