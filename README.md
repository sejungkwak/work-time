# WORK TIME - Employee Time Management System

_WORK TIME_ is an employee time management system which runs in an SSH terminal in a browser. The application will be targeted towards small business owners that are looking for an effective way to manage their employees' schedules. It provides an employee clocking system, attendance tracking and absence management.

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

[Deployment](#deployment)
- [Heroku](#heroku)

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

<br>

# Technical Design

## Flowchart

![Flowchart](documentation/technical-design/flowchart.png)

## Data Model

_Google Sheets_ was chosen to store and retrieve data as most small/start-up companies typically have this tool available and the volume of the data for this project will be small. The python implementation will be able to support a SQL or NoSQL database with minimal refactoring when the volume of data requires it.
The spreadsheet has 5 main worksheets: login_credentials, employees, clockings, absences and entitlements and 1 supporting worksheet for reporting issues to the system administrator.
 
Each employee’s login id will be stored in the login_credentials sheet and will be the key to link to other worksheets to CRUD(create, read, update, delete) data when the user interacts with the application.
 
I have created a diagram to visualise each sheet and its columns.
 
![Data model](documentation/technical-design/data-model.png)

<br>

# Deployment

## Heroku

This project was deployed automatically from _GitHub_ to _Heroku_ using the following steps:

1. Run the following command in the Terminal to add a list of dependencies to the requirements.txt file. It enables the application to run on Heroku.
`pip3 freeze > requirements.txt`

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

7. Copy the entire creds.json file.
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

<br>
