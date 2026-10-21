# SmartAttend

#### Video Demo: TODO

#### Description:

SmartAttend is a web-based event attendance management system that
uses **QR codes** to simplify the process of recording and managing
attendance. It is designed to help event organizers manage attendance
without relying on manually maintained paper registers or spreadsheets.

Traditional attendance-taking can be time-consuming, especially when
many people attend an event. Recording names manually can also lead to
duplicate entries and make it difficult to organize attendance records.
SmartAttend addresses these problems by allowing organizers to create
events, generate QR codes for check-ins, and maintain attendance records
in a centralized database.

<center><img src="src/static/images/logo.svg" style="text-align: center;" /></center>

## Features

### Organizer Authentication

Organizers can create accounts and log in to access their dashboards.
Passwords are hashed before being stored in the database. Session-based
authentication allows the application to identify logged-in organizers
across requests.

### Event Management

![Event Management Image 1](src/static/images/features/dashboard.png)
![Event Management Image 2](src/static/images/features/edit_events.png)

Authenticated organizers can create events and manage their availability.
Each event has a unique token used to identify it during QR-code check-in.
Event ownership is checked before allowing access to organizer-specific
operations.

### QR-Code Attendance

![QR-Code Attendance Image](src/static/images/features/view_event.png)

SmartAttend generates a QR code associated with each event. Attendees
can scan the code to open the check-in page and submit their details.
The application records successful check-ins in the database and
prevents duplicate attendance entries for the same event and email
address.

### Attendance Records

![Attendance Records Image](src/static/images/features/attendee_info.png)

Attendance records are associated with their corresponding events.
Organizers can view or export attendance information _(in .csv format)_, depending on
the features enabled in the application.

## Technologies Used

- **Python _(3.14.4)_:** _Application logic and backend development._
- **FastAPI:** _HTTP routing and request handling._
- **Jinja2:** _Server-side rendering of HTML templates._
- **SQLAlchemy:** _Database models and database operations._
- **MySQL:** _Persistent storage for organizers, events, and attendance._
- **HTML and CSS:** _Page structure and styling._
- **JavaScript:** _Client-side interactions._
- **QRCode _(Python library)_:** _QR-code generation._
- **Uvicorn:** _Development and application server._
- _Other Python libraries used by this project are listed in [requirements.txt](requirements.txt)_

## Project / Repository Structure

<small>_(Tree structre below generated using `tree` in )_</small>

```
.
├── README.md
├── requirements.txt
└── src
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    ├── security.py
    ├── static
    │   ├── css
    │   │   ├── dashboard.css
    │   │   └── style.css
    │   ├── images
    │   │   ├── features
    │   │   │   ├── attendee_info.png
    │   │   │   ├── dashboard.png
    │   │   │   ├── delete_settings.png
    │   │   │   ├── edit_events.png
    │   │   │   └── view_event.png
    │   │   ├── logo.png
    │   │   └── logo.svg
    │   ├── js
    │   │   ├── dashboard.js
    │   │   └── main.js
    │   └── qrcodes
    ├── templates
    │   ├── base.html
    │   ├── checkin.html
    │   ├── create_event.html
    │   ├── dashboard.html
    │   ├── index.html
    │   ├── login.html
    │   ├── manage_event.html
    │   ├── message.html
    │   ├── register.html
    │   ├── settings.html
    │   └── view_event.html
    └── utils.py

9 directories, 30 files

```
