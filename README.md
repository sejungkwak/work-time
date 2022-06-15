# WORK TIME - Employee Time Management System

_WORK TIME_ is an employee time management system which runs in an SSH terminal in a browser. The application will be targeted towards small business owners that are looking for an effective way to manage their employees' schedules. It provides an employee clocking system, attendance tracking and absence management.

![Main Title Screenshot](documentation/title-screen.png)

### View the live project [here](https://work--time.herokuapp.com/)

__NOTE__: This application can only be operated properly on a desktop computer browser.

<br>

# Table of Contents

[User Experience (UX)](#user-experience-ux)
- [Application Goals](#application-goals)
- [Target Audience](#target-audience)
- [User Stories](#user-stories)
- [Strategy Table / Diagram](#strategy-table--diagram)
- [Application Structure](#application-structure)
- [Wireframe](#wireframe)

[Technical Design](#technical-design)
- [Flowchart](#flowchart)
- [Data Model](#data-model)

[Technologies Used](#technologies-used)
- [Languages](#languages)
- [Libraries](#libraries)
- [Programs](#programs)

[Testing](#testing)
- [Testing User Stories](#testing-user-stories-from-the-user-experience-ux-section)

[Deployment](#deployment)
- [Heroku](#heroku)
- [Making a Local Clone](#making-a-local-clone)
- [Forking this Repository](#forking-this-repository)

[Credits](#credits)
- [Code](#code)
- [Inspiration](#inspiration)
- [Acknowledgements](#acknowledgements)

<br>

# User Experience (UX)

## Application Goals

- To provide a time management system that optimises the productivity of employees by automating idle routines such as recording clocking times, time-off entitlements and group absences.
- To deliver information as intuitively as possible by providing descriptive messages and a clear content structure.

## Target Audience

small business owners, supervisors and their employees

## User Stories

- As a superuser (business owner / supervisor),
    - I want the login credentials to be secure so that an unauthorised person cannot access the admin account.
    - I want to be able to reset my password so that I can access the system even when I forget it.
    - I want to be able to review each employee's attendance record so that I can manage the team more effectively.
    - I want to be able to review a list of all requests easily so that I don't miss anything.
    - I want to be able to see the team's availability so that I can easily determine whether I can approve or reject new absence requests.
    - I want to be notified when there's a new request so that I can proceed as soon as possible.
    - I want the system to programmatically generate payslips so that I can avoid idle and error-prone routines.
    - I want to be able to add a new employee to the system so that they can start using the system immediately.

<br>

- As a user (employee),
    - I want a simple log-in process so that I can complete my task as quickly as possible.
    - I want an easy to use system so that I can complete my task as quickly as possible.
    - I want to be able to check my absence entitlements so that I can plan my holidays as quickly as possible.
    - I want to be able to book and cancel my holidays on the system so that I don't have to email my manager or update it on the Excel spreadsheet.
    - I want to be able to review worked hours so that I can flag it to the manager immediately if it's inaccurate.
    - I want to be able to check who's out of the office at a glance so that I can arrange meetings / events on a day when the relevant members are in.

## Strategy Table / Diagram

The strategy table and diagram have been created to decide on what features should be implemented in this project. The listed features are based on the user stories. Each feature's importance and viability / feasibility were rated on a scale of 1 to 5 where 5 is the most important and the most viable / feasible.

![Strategy Table and Diagram](documentation/ux/strategy-plane.png)

## Application Structure

Based on the strategy rating, I have decided to implement the following features: Log in(Feature ID 1), Clock in/out(3), Book/Cancel/Approve/Reject time-off(4), Review Clock in/out time(7), Review absence entitlements(8), Review group absence(9).

The application will be structured as shown in the following diagram.

![Application Structure](documentation/ux/structure.png)

## Wireframe

![Wireframe](documentation/ux/wireframe.png)

[Back To **Table of Contents**](#table-of-contents)

<br>

# Technical Design

## Flowchart

![Flowchart](documentation/technical-design/flowchart.png)

## Data Model

_Google Sheets_ was chosen to store and retrieve data as most small/start-up companies typically have this tool available and the volume of the data for this project will be small. The python implementation will be able to support a SQL or NoSQL database with minimal refactoring when the volume of data requires it.
The spreadsheet has 5 worksheets: login_credentials, employees, clockings, absences_requests and entitlements.
 
Each employee’s login id will be stored in the login_credentials sheet and will be the key to link to other worksheets to CRUD(create, read, update, delete) data when the user interacts with the application.
 
I have created a diagram to visualise each sheet and its columns.

![Data model](documentation/technical-design/data-model.png)

The spreadsheet can be found [here](https://docs.google.com/spreadsheets/d/1yBUMfb2aVQdtDsvj2FyMLVSAgK2HFpPF_FO3ZXAN37s/edit?usp=sharing)

[Back To **Table of Contents**](#table-of-contents)

<br>

# Technologies Used

## Languages

- [Python](https://www.python.org/) was used as the main scripting language.
- [HTML5](https://en.wikipedia.org/wiki/HTML5) was used to embed the calendar iframe.*
- [CSS3](https://en.wikipedia.org/wiki/CSS) was used to style the layout of elements to the centre and adjust the terminal height.*
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript) was used to auto-refresh the calendar.*

    *This project used the _Code Institute_ Python template to display a simulated terminal. Other than the code mentioned, all code is part of the template.

## Libraries

### Built-in Modules

- [datetime](https://docs.python.org/3/library/datetime.html) was used to get the current year, date and time as well as calculate (week)days between two dates.
- [enum](https://docs.python.org/3/library/enum.html) was used to create enumerated constants for the colorama font colours.
- [itertools](https://docs.python.org/3/library/itertools.html) was used to group a list of lists by employee IDs.
- [os](https://docs.python.org/3/library/os.html) was used to clear the terminal.
- [sys](https://docs.python.org/3/library/sys.html) was used to exit the system for the KeyboardInterrupt exception.
- [time](https://docs.python.org/3/library/time.html) was used to add delay in the execution before clearing the screen.

### Third-party Packages

- [colorama](https://pypi.org/project/colorama/) was used to highlight texts by printing in different colours.
- [google-auth](https://google-auth.readthedocs.io/en/master/) was used to authenticate for the Google APIs.
- [gspread](https://docs.gspread.org/en/v5.3.2/#) was used to access and manipulate data in Google Sheets.
- [passlib](https://passlib.readthedocs.io/en/stable/) was used to store users’ passwords securely.
- [pytz](https://pypi.org/project/pytz/) was used to set a Timezone to Dublin, Ireland.
- [stdiomask](https://pypi.org/project/stdiomask/) was used for password masking.
- [tabulate](https://pypi.org/project/tabulate/) was used to display tables.

## Programs

- [Balsamiq](https://balsamiq.com/) was used to create the wireframes.
- [Canva](https://www.canva.com/) was used to create the strategy table and diagram, and design the favicon.
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/) was used to check runtime performance.
- [Diagrams.net](https://app.diagrams.net/) was used to create the flowchart and diagrams.
- [Favicon.io](https://favicon.io/) was used to create the favicon.
- [Git](https://git-scm.com/) was used for version control.
- [GitHub](https://github.com/) was used to store the project's code and link to Heroku for auto-deployment. Its project board was also used to organise the list of work separated into documentation(README), development and bug fix and prioritise the work.
- [Gitpod](https://www.gitpod.io/) was used to develop and test my code.
- [Google Apps Script](https://developers.google.com/apps-script) was used to write code to enable updating the calendar from the absence_requests worksheet.
- [Google Calendar](https://www.google.com/calendar/about/) was used to embed the calendar in `index.html`.
- [Google Sheets](https://www.google.com/sheets/about/) was used to create/read/update/delete all data.
- [Grammarly](https://app.grammarly.com/) was used to check for errors in the README.
- [PEP8](http://pep8online.com/) was used to check the Python script validity.
- [Text to ASCII Art Generator (TAAG)](https://patorjk.com/software/taag/) was used for the title text: “Work Time”, “Admin Portal”, “Employee Portal” and “Goodbye” in ANSI Regular(font name).
- [Visual Studio Code](https://code.visualstudio.com/) was used to edit my code.
- [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used to check the CSS validity.
- [W3C Markup Validation Service](https://validator.w3.org/) was used to check the HTML markup validity.
- [Zapier](https://zapier.com/) was used to send notifications for new absence requests automatically.

[Back To **Table of Contents**](#table-of-contents)

<br>

# Testing

## Testing User Stories from the User Experience (UX) Section

- As a superuser (business owner / supervisor),

    - [x] I want the login credentials to be secure so that an unauthorised person cannot access the admin account.

        : Stored passwords are hashed and salted using a password hashing library called [Passlib](https://passlib.readthedocs.io/en/stable/).

    - [ ] I want to be able to reset my password so that I can access the system even when I forget it.

        : This feature has not been implemented as mentioned in the [UX strategy section](#strategy-table--diagram). Its importance and viability/feasibility ratings were low to deliver a minimum viable product.

    - [x] I want to be able to review each employee's attendance record so that I can manage the team more effectively.

        : The admin can review all employee’s clock cards for the current day by typing 2 at the admin portal menu. They can type in another day to review them.

        <details>
            <summary>Attendance Review Screenshot</summary>
            <img src="documentation/testing/ux/superuser-attendance.png">
        </details>

    - [x] I want to be able to review a list of all requests easily so that I don't miss anything.

        : Upon login to the admin portal, a request notification displays on top of the menu advising of any new absence requests. The admin can review new absence requests by typing 1 at the admin portal menu.

        <details>
            <summary>Request Notification and Review Requests Screenshot</summary>
            <img src="documentation/testing/ux/superuser-notification_portal.png">
            <img src="documentation/testing/ux/superuser-review-requests.png">
        </details>

    - [x] I want to be able to see the team's availability so that I can easily determine whether I can approve or reject new absence requests.

        : The calendar displays all employees’ absence schedules that have been approved by the admin.

        <details>
            <summary>Group Absence Calendar Screenshot</summary>
            <img src="documentation/testing/ux/superuser-calendar.png">
        </details>

    - [x] I want to be notified when there's a new request so that I can proceed as soon as possible.

        : An email is sent to the admin automatically when a new row is appended in the `absence_requests` worksheet using [Zapier](https://zapier.com/) service.

        <details>
            <summary>Request Notification Email Screenshot</summary>
            <img src="documentation/testing/ux/superuser-notification_email.png">
        </details>

    - [ ] I want the system to programmatically generate payslips so that I can avoid idle and error-prone routines.

        : This feature has not been implemented as mentioned in the [UX strategy section](#strategy-table--diagram). Its importance and viability/feasibility ratings were low to deliver a minimum viable product.

    - [ ] I want to be able to add a new employee to the system so that they can start using the system immediately.

        : This feature has not been implemented as mentioned in the [UX strategy section](#strategy-table--diagram). Its importance and viability/feasibility ratings were low to deliver a minimum viable product.

<br>

- As a user (employee),

    - [x] I want a simple log-in process so that I can complete my task as quickly as possible.

        : The system only requires an employee ID and its associated password to log in.

    - [x] I want an easy to use system so that I can complete my task as quickly as possible.

        : The application offers clear menu options and guided questions with detailed instructions.

    - [x] I want to be able to check my absence entitlements so that I can plan my holidays as quickly as possible.

        : The user can review their absence entitlements by typing 4 at the employee portal menu. The absence entitlements display in a table with total, taken, planned, pending and unallocated hours.

        <details>
            <summary>Absence Entitlements Screenshot</summary>
            <img src="documentation/testing/ux/user-entitlements.png">
        </details>

    - [x] I want to be able to book and cancel my holidays on the system so that I don't have to email my manager or update it on the Excel spreadsheet.

        : The user can easily cancel their planned/pending absence by typing 6 at the employee portal menu.

        <details>
            <summary>Absence Cancellation Screenshot</summary>
            <img src="documentation/testing/ux/user-cancel-absence-step1.png">
            <img src="documentation/testing/ux/user-cancel-absence-step2.png">
        </details>

    - [x] I want to be able to review worked hours so that I can flag it to the manager immediately if it's inaccurate.

        : The user can view their clock in and clock out times by typing 3 at the employee portal menu. The information displays a week at a time in a table and the default display is the current week. The user can type in a different date to view another week’s clock cards.

        <details>
            <summary>Clock cards Screenshot</summary>
            <img src="documentation/testing/ux/user-attendance.png">
        </details>

    - [x] I want to be able to check who's out of the office at a glance so that I can arrange meetings / events on a day when the relevant members are in.

        : The calendar displays all employee’s absence schedules that have been approved by the admin.

[Back To **Table of Contents**](#table-of-contents)

<br>

# Deployment

## Heroku

This project was deployed automatically from _GitHub_ to _Heroku_ using the following steps:

1. Run the following command in the Terminal to add a list of dependencies to the requirements.txt file. It enables the application to run on Heroku.

    ```
    pip3 freeze > requirements.txt
    ```

    <details>
        <summary>Deployment Step 1 Screenshot</summary>
        <img src="documentation/deployment/deployment-step1.png">
    </details>

2. Go to the _Heroku_ website and log in to my account.
3. Click the __New__ button on the dashboard.
4. Select the __Create new app__ option.

    <details>
        <summary>Deployment Step 3 and Step 4 Screenshot</summary>
        <img src="documentation/deployment/deployment-step3-4.png">
    </details>

5. Fill in the form and click the __Create app__ button.

    <details>
        <summary>Deployment Step 5 Screenshot</summary>
        <img src="documentation/deployment/deployment-step5.png">
    </details>

6. Go to __Settings__ and click the __Reveal Config Vars__ button.

    <details>
        <summary>Deployment Step 6 Screenshot</summary>
        <img src="documentation/deployment/deployment-step6.png">
    </details>

7. Copy the entire `creds.json` file.
8. Input __CREDS__ in the key field, paste the copied text in step 7 to the value field and then click the __ADD__ button.

    <details>
        <summary>Deployment Step 8 Screenshot</summary>
        <img src="documentation/deployment/deployment-step8.png">
    </details>

9. Scroll down to the __Buildpacks__ section and click the __Add buildpack__ button.

    <details>
        <summary>Deployment Step 9 Screenshot</summary>
        <img src="documentation/deployment/deployment-step9.png">
    </details>

10. Select __python__ and click the __Save changes__ button.

    <details>
        <summary>Deployment Step 10 Screenshot</summary>
        <img src="documentation/deployment/deployment-step10.png">
    </details>

11. Repeat step 9.

12. Select __nodejs__ and click the __Save changes__ button.

    <details>
        <summary>Deployment Step 12 Screenshot</summary>
        <img src="documentation/deployment/deployment-step12.png">
    </details>

13. Scroll up and select __Deploy__.
14. Select __GitHub__ in the __Deployment method__ section.
15. Click __Connect to GitHub__.

    <details>
        <summary>Deployment Step 13 to Step 15 Screenshot</summary>
        <img src="documentation/deployment/deployment-step13-15.png">
    </details>

16. Enter this repository name and click __Search__.
17. When the repository with __Connect__ button appears, click the button.

    <details>
        <summary>Deployment Step 16 and Step 17 Screenshot</summary>
        <img src="documentation/deployment/deployment-step16-17.png">
    </details>

18. The status changes to connected.

    <details>
        <summary>Deployment Step 18 Screenshot</summary>
        <img src="documentation/deployment/deployment-step18.png">
    </details>

19. Click __Enable Automatic Deploys__.

    <details>
        <summary>Deployment Step 19 Screenshot</summary>
        <img src="documentation/deployment/deployment-step19.png">
    </details>

20. The text changes to indicate that automatic deploys are enabled successfully.

    <details>
        <summary>Deployment Step 20 Screenshot</summary>
        <img src="documentation/deployment/deployment-step20.png">
    </details>

## Making a Local Clone

These steps demonstrate how I cloned my repository to create a local copy on my computer to run the code locally.

1. Navigate to [my GitHub Repository](https://github.com/sejungkwak/work-time).
2. Click the __Code__ button above the list of files.

    <details>
        <summary>Clone Step 1 and Step 2 Screenshot</summary>
        <img src="documentation/deployment/clone-step1-2.png">
    </details>

3. Select __HTTPS__ under __Clone__. I have chosen this option as it is simpler than SSH.
4. Click the copy icon on the right side of the URL.

    <details>
        <summary>Clone Step 3 and Step 4 Screenshot</summary>
        <img src="documentation/deployment/clone-step3-4.png">
    </details>

5. Open the Terminal.
6. Change the current working directory to the location where I want the cloned directory.
7. Type `git clone ` and then paste the URL I copied in step 4.

    ```
    git clone https://github.com/sejungkwak/work-time.git
    ```

    <details>
        <summary>Clone Step 6 and Step 7 Screenshot</summary>
        <img src="documentation/deployment/clone-step6-7.png">
    </details>

8. Press enter. Messages are displayed in the Terminal to indicate the local clone has been successfully created.

    <details>
        <summary>Clone Step 8 Screenshot</summary>
        <img src="documentation/deployment/clone-step8.png">
    </details>

9. Copy the existing service account key from the `creds.json` file.
10. Create a new file called `creds.json` in the root directory and then paste the key I copied in step 9.

## Forking this Repository

These steps demonstrate how to make a copy of this repository on your _GitHub_ account to make changes without affecting this repository or to deploy the site yourself.

1. Log in to your _GitHub_ account.
2. Navigate to [this Work Time repository](https://github.com/sejungkwak/work-time).
3. Click the __fork__ button on the top right side of the repository.

    <details>
        <summary>Fork Step 3 Screenshot</summary>
        <img src="documentation/deployment/fork.png">
        The button in the image is disabled since the repository belongs to me. It should be active if you logged on your account.
    </details>

4. You should now have a copy of this repository in your _GitHub_ account.

    To make the application work, a few more steps are required.

5. Go to [_Google Cloud Platform_](https://console.cloud.google.com).
6. Create a new project and enable three APIs: _Google Drive_, _Google Sheets_ and _Google Calendar_.
7. Generate service account credentials and download the JSON file.
8. Add the downloaded JSON file to the root directory and rename it `creds.json`.
9. Copy the value of `client_email` in `creds.json`.
10. Make a copy of [this project's spreadsheet](https://docs.google.com/spreadsheets/d/1yBUMfb2aVQdtDsvj2FyMLVSAgK2HFpPF_FO3ZXAN37s/edit?usp=sharing).
11. Click __Share__ and paste `client_email` you copied in step 9 as an Editor.
12. Replace the calendar link with your own calendar in `views/layout.html`.
13. Run the following command in the Terminal to install dependencies listed in `requirements.txt`.

    ```
    pip3 install -r requirements.txt
    ```

14. You can make a local clone from the copied repository on your computer using the steps demonstrated in [Making a Local Clone](#making-a-local-clone) and/or deploy to _Heroku_ using the steps demonstrated in [Heroku](#heroku).

[Back To **Table of Contents**](#table-of-contents)

<br>

# Credits

## Code

- I highly relied upon the [Python documentation](https://docs.python.org/3/) for Python built-in modules’ usages and the [gspread documentation](https://docs.gspread.org/en/v5.4.0/) for _Google Sheets_ API’s usages.
- I referenced the [W3schools](https://www.w3schools.com/) and [Stack Overflow](https://stackoverflow.com/) to find appropriate modules or solutions for specific issues.

- Clearing the terminal
    - Source: GeeksforGeeks’s article [How to clear screen in python?](https://www.geeksforgeeks.org/clear-screen-python/)
    - Method: Defining a function to clearing the terminal using the `os` module.
    - Usage: I used this method to clear the terminal after user input.

- Sorting a list of lists by an index
    - Source: mouad's answer on [Stack Overflow](https://stackoverflow.com/questions/4174941)
    - Method: Sorting a list of lists by a specific index using `sort` and `lambda`.
    - Usage: I used this method to sort a list of lists containing new absence requests for the admin portal before grouping them into another list.

- Grouping lists by a value
    - Source: Robert Rossney's answer on [Stack Overflow](https://stackoverflow.com/questions/5695208)
    - Method: Grouping lists by a specific value using `itertools.groupby`.
    - Usage: I used this method to group new requests by an employee to fix an issue on a table width.

- Docstrings
    - Source: [_Google_ Python Style Guide](https://google.github.io/styleguide/pyguide.html)
    - Usage: I used the _Google_’s docstring style. I found its format is the most readable style because of the indentation after I read daouzli’s answer on [Stack Overflow](https://stackoverflow.com/questions/3898572).

- Auto-refresh iframe / JavaScript
    - Source: Vikas Sardana's answer on [Stack Overflow](https://stackoverflow.com/questions/43661695/)
    - Method: Refresh the iframe automatically every certain time using `setInterval` and set the `src` attribute again inside the `setInterval`’s callback function.
    - Usage: I used this method to refresh the calendar every 20 seconds as otherwise the page needs to be reloaded to see the updated calendar.

- Displaying a favicon / HTML
    - Source: `layout.html` on MattBCoding’s repository [calico-jack](https://github.com/MattBCoding/calico-jack/blob/main/views/layout.html)
    - Method: Using a web-hosted file enables the display of the favicon.
    - Usage: I used this method to fix an issue where the static favicon file did not display.

## Inspiration

- Employee time management system

    I developed the idea of building this project from a software company [Mitrefinch](https://www.mitrefinch.co.uk/)’s time management system that I use at work.

## Acknowledgements

- My fiancé Ciarán Maher for his feedback and proofreading.
- My friends Hwayoung Kim, Junga Choi, Sena Park and Haeyoung Lee for testing the project.
- My mentor Narender Singh for his guidance and advice.
- My Cohort Facilitator Kasia Bogucka at Code Institute for the help.

[Back To **Table of Contents**](#table-of-contents)