# Table of Contents

[Login](#login)

[Employee Portal](#employee-portal)

[Admin Portal](#admin-portal)

Please refer to [this spreadsheet](https://docs.google.com/spreadsheets/d/1BLCJERy2hTPUg31x8aWZ-jE71pDdTzyrFN84NnpgFPg/edit?pli=1#gid=0) for more details.

## Login

| Input | Expected result | Actual result | Test result |
| :--: | :--: | :--: | :--: |
| Valid ID | Prompt for Password | Prompt for Password | Pass |
| Type __help__ | Display application information | Display application information | Pass |
| Invalid ID | Display error message | Display error message | Pass |
| Valid Password | Log into the admin/employee portal | Log into the admin/employee portal | Pass |
| Invalid Password | Display error message | Display error message | Pass |

[Back To __Table of Contents__](#table-of-contents)

<br>

## Employee Portal

- Menu
    > 1. Clock In
    > 2. Clock Out
    > 3. View Clock Card
    > 4. View Absence Entitlements
    > 5. Book Absence
    > 6. Cancel Absence
    > 7. Exit

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __1__ | Clock In | Clock In | Pass |
    | Press __2__ | Clock Out | Clock Out | Pass |
    | Press __3__ | Display the current week's clock card | Display the current week's clock card | Pass |
    | Press __4__ | Display the absence entitlements | Display the absence entitlements | Pass |
    | Press __5__ | Go to Book Absence option | Go to Book Absence option | Pass |
    | Press __6__ | Go to Cancel Absence option | Go to Cancel Absence option | Pass |
    | Press __7__ | Exit the system | Exit the system | Pass |
    | Press __8__ | Display error message | Display error message | Pass |

- Option 1. Clock In 

    > Already clocked in for today. Overwrite it?

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __y__ | Update the clock in time to worksheet | Update the clock in time to worksheet | Pass |
    | Press __n__ | No changes | No changes | Pass |
    | Press __yes__ | Display error message | Display error message | Pass |

- Option 3. View Clock Card

    > Enter a date to review another week's clock cards.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid date & format | Display clock card | Display clock card | Pass |
    | Invalid date or format | Display error message | Display error message | Pass |

- Option 5. Book Absence

    > 1. 9:30AM-1:30PM
    > 2. 1:30PM-5:30PM
    > 3. Full day
    > 4. More than 2 consecutive days

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __1__ or __2__ or __3__ or __4__ | Prompt for date | Prompt for date | Pass |
    | Press __5__ | Display error message | Display error message | Pass |

    > Enter the absence (start / last) date.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid date & format | Display summary for confirmation | Display summary for confirmation | Pass |
    | Invalid date or format | Display error message | Display error message | Pass |

    > Submit this request?

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __y__ | Add data to worksheet | Add data to worksheet | Pass |
    | Press __n__ | No changes | No changes | Pass |
    | Press __yes__ | Display error message | Display error message | Pass |

- Option 6. Cancel Absence

    > Enter a request ID to cancel.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid request ID | Display summary for confirmation | Display summary for confirmation | Pass |
    | Invalid request ID | Display error message | Display error message | Pass | 

    > Cancel this absence?

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __y__ | Update data to worksheet | Update data to worksheet | Pass |
    | Press __n__ | No changes | No changes | Pass |
    | Press __yes__ | Display error message | Display error message | Pass |

[Back To __Table of Contents__](#table-of-contents)

<br>

## Admin Portal

- Menu
    > 1. Review Requests
    > 2. Review Attendance
    > 3. Add Absence
    > 4. Update Clock Card
    > 5. Exit

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __1__ | Display new requests | Display new requests | Pass |
    | Press __2__ | Display today's clock cards | Display today's clock cards | Pass |
    | Press __3__ | Go to Add Absence option | Go to Add Absence option | Pass |
    | Press __4__ | Go to Update Clock Card option | Go to Update Clock Card option | Pass |
    | Press __5__ | Exit the system | Exit the system | Pass |
    | Press __6__ | Display error message | Display error message | Pass |

- Option 1. Review Requests

    > Enter a request ID to approve or reject.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid request ID | Prompt for decison | Prompt for decison | Pass |
    | Invalid request ID | Display error message | Display error message | Pass |

    > Enter __approve__ or __reject__.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Type __approve__ or __reject__ | Display summary for confirmation | Display summary for confirmation | Pass |
    | Invalid input | Display error message | Display error message | Pass |

    > Approve/Reject this request?

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __y__ | Update data to worksheet | Update data to worksheet | Pass |
    | Press __n__ | No changes | No changes | Pass |
    | Press __yes__ | Display error message | Display error message | Pass |

- Option 2. Review Attendance

    > Enter a date to review another day's clock cards.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid date & format | Display clock cards | Display clock cards | Pass |
    | Invalid date or format | Display error message | Display error message | Pass |

- OPtion 3. Add Absence

    > Enter an employee ID.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid employee ID | Prompt for paid type | Prompt for paid type | Pass |
    | Invalid employee ID | Display error message | Display error message | Pass |

    > 1. Paid
    > 2. Unpaid

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __1__ or __2__ | Prompt for duration | Prompt for duration | Pass |
    | Press __3__ | Display error message | Display error message | Pass |

    > 1. 9:30AM-1:30PM
    > 2. 1:30PM-5:30PM
    > 3. Full day
    > 4. More than 2 consecutive days

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __1__ or __2__ or __3__ or __4__ | Prompt for date | Prompt for date | Pass |
    | Press __5__ | Display error message | Display error message | Pass |

    > Enter the absence (start / last) date.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid date & format | Display summary for confirmation | Display summary for confirmation | Pass |
    | Invalid date or format | Display error message | Display error message | Pass |

    > Update this absence?

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __y__ | Update data to worksheet | Update data to worksheet | Pass |
    | Press __n__ | No changes | No changes | Pass |
    | Press __yes__ | Display error message | Display error message | Pass |

- OPtion 4. Update Clock Card

    > Enter an employee ID.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid employee ID | Prompt for date | Prompt for date | Pass |
    | Invalid employee ID | Display error message | Display error message | Pass |

    > Enter a date.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid date & format | Prompt for type | Prompt for type | Pass |
    | Invalid date or format | Display error message | Display error message | Pass |

    > 1. Clock In
    > 2. Clock Out

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __1__ or __2__ | Prompt for time | Prompt for time | Pass |
    | Press __3__ | Display error message | Display error message | Pass |

    > Enter a time.

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Valid time & format | Display summary for confirmation | Display summary for confirmation | Pass |
    | Invalid time or format | Display error message | Display error message | Pass |

    > Update?

    | Input | Expected result | Actual result | Test result |
    | :--: | :--: | :--: | :--: |
    | Press __y__ | Update data to worksheet | Update data to worksheet | Pass |
    | Press __n__ | No changes | No changes | Pass |
    | Press __yes__ | Display error message | Display error message | Pass |

[Back To __Table of Contents__](#table-of-contents)