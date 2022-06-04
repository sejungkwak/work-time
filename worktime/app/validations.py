# Third-party Packages
from passlib.hash import pbkdf2_sha256

# Custom Packages
from worktime.app import utility
from worktime.worksheets import credentials


def validate_id(id):
    """Retrieve a list of IDs and check if the given ID is on the list.

    Args:
        :id str: An employee ID.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If the ID is not on the ID list.
    """
    try:
        ids = credentials.Credentials().ids()
        if id not in ids:
            raise ValueError()
    except ValueError:
        print(f"\nYou have entered an invalid ID: {id}.\nPlease try again!\n")
        return False
    else:
        return True


def validate_pw(id, entered_pw):
    """Retrieve the password for the id and check if the given password is correct.

    Args:
        :id str: An employee ID.
        :entered_pw str: A password the user has inputted.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If the input password does not match.
    """
    try:
        password = credentials.Credentials().pw(id)
        valid = pbkdf2_sha256.verify(entered_pw, password)
        if not valid:
            raise ValueError()
    except ValueError:
        print(f"\nYou have entered an incorrect password.\nPlease try again!")
        return False
    else:
        return True


def validate_choice_number(choice, numbers):
    """Convert a string value into an integer.

    Args:
        :choice str: A number the user has inputted.
        :numbers list: Numbered options.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If the input value is not a digit or out of range.
    """
    try:
        choice = int(choice)
        if choice not in numbers:
            raise ValueError()
    except ValueError:
        print(f"You have entered an invalid value: {choice}.",
              "\nPlease try again!")
        return False
    else:
        return True


def validate_choice_yesno(choice):
    """Check if the user entered y or n.

    Args:
        :choice str: A letter the user has inputted.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If the input value is not y or n.
    """
    try:
        if choice not in ["Y", "N"]:
            raise ValueError()
    except ValueError:
        print(f"You have entered an invalid value: {choice}.",
              "\nPlease try again!")
        return False
    else:
        return True


def validate_date(date):
    """Pass the argument to the convert_date function.
    Convert_date splits a string into a list of integers that represent
    year, month and date, and then pass them to the datetime.date() object.

    Args:
        :date str: A value the user has entered for the date.

    Returns:
        class: A ISO format date if successful.
        bool: False if exceptions raised.

    Raises:
        ValueError: If the date is invalid.
        IndexError: If "/" is not used to separate the year, month and date.
    """
    try:
        date = utility.convert_date(date)
    except (ValueError, IndexError):
        print("Please provide a valid date with the correct format.")
        return False
    else:
        return date


def validate_days(date1, date2, unallocated):
    """Calculate total number of weekdays and check if it is a positive number
    and greater than unallocated.

    Args:
        :date1: Absence start date
        :date2: Absence end date
        :unallocated: Total available hours

    Returns:
        int: Total number of weekdays between date1 and date2.
        bool: False if exceptions raised.

    Raises:
        ValueError: If request hours are exceed the unallocated hours
                    or the end date is before start date.
    """
    try:
        start_date = utility.convert_date(date1)
        end_date = utility.convert_date(date2)
        num_of_days = utility.get_num_of_weekdays(start_date, end_date)
        num_of_hours = num_of_days * 8
        if num_of_hours > int(unallocated):
            raise ValueError(
                print("You have unsufficient paid time off available.")
            )
        if num_of_days < 0:
            raise ValueError(
                print("Please make sure to enter the dates correctly.")
            )
    except ValueError:
        return False
    else:
        return num_of_days
