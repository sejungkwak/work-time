# Third-party Packages
from passlib.hash import pbkdf2_sha256

# Custom Packages
from worktime.app import utility


def validate_id(id, ids):
    """In the try block, compare the given ID to the list of IDs.

    Args:
        id str: An employee ID.
        ids list: Employee IDs with matching password.
    Returns:
        bool: True if the ID in the list, False otherwise.
    Raises:
        ValueError: If the ID is not in the ID list.
    """
    try:
        if id not in ids:
            raise ValueError()
    except ValueError:
        print(utility.red("Invalid ID: " + id))
        return False
    else:
        return True


def validate_pw(id, entered_pw, password):
    """In the try block, check if the given password is correct
    using passlib method.

    Args:
        id str: An employee ID.
        entered_pw str: A password the user has inputted.
        password: The correct password.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ValueError: If the input password does not match.
    """
    try:
        valid = pbkdf2_sha256.verify(entered_pw, password)
        if not valid:
            raise ValueError()
    except ValueError:
        print(utility.red("Incorrect password."))
        return False
    else:
        return True


def validate_choice_number(choice, numbers):
    """In the try block, convert a string value into an integer.

    Args:
        choice str: A number the user has inputted.
        numbers list: Numbered options.
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
        print(utility.red("Invalid value: " + str(choice)))
        return False
    else:
        return True


def validate_choice_letter(choice, choices):
    """In the try block, check if the user entered a valid input.

    Args:
        choice str: A letter the user has inputted.
        choices list: A list of options the user needs to choose from.
    Returns:
        bool: True if successful, False otherwise.
    Raises:
        ValueError: If the input value is not in the list.
    """
    try:
        if choice not in choices:
            raise ValueError()
    except ValueError:
        print(utility.red("Invalid value: " + choice))
        return False
    else:
        return True


def validate_date(date):
    """In the try block, pass the argument to the convert_date function.

    Args:
        date str: A value the user has entered for the date.
    Returns:
        date: A ISO format date if successful.
        bool: False if exceptions raised.
    Raises:
        ValueError: If the date is invalid.
        IndexError: If "/" is not used to separate the year, month and date.
    """
    try:
        date = utility.convert_date(date)
    except ValueError:
        print(utility.red("Invalid date: " + str(date)))
        return False
    except IndexError:
        print(utility.red("Invalid format: " + str(date)))
        return False
    else:
        return date


def validate_days(date1, date2, unallocated):
    """In the try block, calculate total number of weekdays between 2 given dates.

    Args:
        date1 str: The start date.
        date2 str: The end date.
        unallocated: Total available absence hours.
    Returns:
        int: Total number of weekdays between date1 and date2.
        bool: False if exceptions raised.
    Raises:
        ValueError: If request hours are exceed the unallocated hours
                    or the end date is before start date.
    """
    try:
        num_of_days = utility.get_num_of_weekdays(date1, date2)
        num_of_hours = num_of_days * 8
        if num_of_hours > int(unallocated):
            raise ValueError(
                print(utility.red("Insufficient paid time off available."))
            )
        elif num_of_days < 2:
            raise ValueError(
                print(utility.red("The end date must be"),
                      utility.red("after the start date."))
            )
    except ValueError:
        return False
    else:
        return num_of_days


def validate_unpaid_days(date1, date2):
    """In the try block, calculate total number of weekdays.

    Args:
        date1 str: The start date.
        date2 str: The end date.
    Returns:
        int: Total number of weekdays between date1 and date2.
        bool: False if exceptions raised.
    Raises:
        ValueError: If the end date is before start date.
    """
    try:
        num_of_days = utility.get_num_of_weekdays(date1, date2)
        if num_of_days < 2:
            raise ValueError(
                print(utility.red("The end date must be"),
                      utility.red("after the start date."))
            )
    except ValueError:
        return False
    else:
        return num_of_days
