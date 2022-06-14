"""Employees Worksheet Module

This module provides functions to retrieve employee ID,
first name and last name.
"""

# Custom Package
from worktime.worksheets import auth


class Employees:
    """Represents the employees worksheet.
        Column A: employee_id
        Column B: first_name
        Column C: last_name

    Args:
        :id str: An employee ID.
    """

    def __init__(self, id_=None):
        self.id_ = id_
        self.worksheet = auth.SHEET.worksheet("employees")
        self.employees = self.worksheet.get_all_values()[1:]

    def get_fname(self):
        """Returns the employee's first name."""
        for employee in self.employees:
            if employee[0] == self.id_:
                fname = employee[1]
        return fname
