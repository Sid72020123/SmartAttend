# SmartAttend

#### Video Demo: [YouTube](https://youtu.be/mLNeryzClB0)

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

---

**Application Favicon:**

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

## Local Installation and Setup

### Prerequisites

Before running SmartAttend, install:

- Python 3.11 or newer. **Python 3.14.4** is the version currently used
  to develop and verify the project. Any version below that are is not tested yet. Python 3.11 is the minimum version allowed by the major dependencies but not verified yet.
- MySQL Server.
- Git, if you are cloning the repository.

### 1. Clone the repository

Clone the repository and navigate to its root directory:

```bash
git clone https://github.com/Sid72020123/SmartAttend.git
cd SmartAttend
```

Alternatively, open your existing SmartAttend project directory in a
terminal.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If the virtual environment is active, your terminal prompt usually
starts with `(.venv)`.

### 3. Install Python dependencies

Upgrade `pip` and install the pinned dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

Start the local MySQL server, then create the SmartAttend database:

```sql
CREATE DATABASE SmartAttend
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Create a dedicated MySQL user for the application and grant it access
to the database:

```sql
CREATE USER 'attendance_user'@'localhost'
IDENTIFIED BY 'YOUR_PASSWORD';

GRANT ALL PRIVILEGES ON SmartAttend.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
```

Do not use the MySQL `root` account as the application's database user.
The application creates its tables automatically when it starts.

### 5. Configure environment variables

Create a `.env` file in the project root, alongside `src/`. Add the
following values and replace the example password and secret:

```dotenv
DATABASE_URL=mysql+pymysql://attendance_user:YOUR_PASSWORD@127.0.0.1:3306/SmartAttend
SESSION_SECRET=YOUR_GENERATED_RANDOM_SECRET
BASE_URL=http://127.0.0.1:8000
COOKIE_SECURE=false
```

If the MySQL password contains characters such as `@`, `:`, `/`, or
`#`, URL-encode the password before placing it in `DATABASE_URL`.

Generate a strong session secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

**Keep `.env` private. It is ignored by Git and must never be committed,
because it contains database credentials and the session secret.**

For local development, `COOKIE_SECURE=false` allows the session cookie
to work over HTTP on localhost. Use HTTPS and set `COOKIE_SECURE=true`
when deploying to production.

### 6. Run the application

From the project root, with the virtual environment active, start the
development server:

```bash
python -m uvicorn src.main:app --reload
```

Open SmartAttend in a browser at:

<http://127.0.0.1:8000>

FastAPI's interactive API documentation is available at:

<http://127.0.0.1:8000/docs>

Press `Ctrl+C` in the terminal to stop the development server.

## Project / Repository Structure

<small>_(Tree structre below was generated using `tree` in `Ubuntu 26.04`)_</small>

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

### Core Python Files:

- All the main code is in [src/](src/) directory of the repository.
- [main.py](src/main.py) - _Defines the necessary `FastAPI` application routes._
- [database.py](src/database.py) - _Creates the `SQLAlchemy` session to make and handle the connection to the DB._
- [models.py](src/models.py) - _Defines the `SQLAlchemy` ORM models to handle the queries to the DB without using `SQL`_
- [schemas.py](src/schemas.py) - _Defines `Pydantic` schemas used to validate or structure application data._
- [security.py](src/security.py) - _Contains secure password hashing and password verification functions._
- [utils.py](src/utils.py) - _Contains a function to make QR codes with the application logo placed at the centre._

### Templates:

- All the `Jinja2` templates required by this project are in [src/templates/](src/templates/) directory.
- It contains a base / main template - [templates/base.html](src/templates/base.html) which is then extended by other templates.
- Following is a brief summary of some main template files:
    - [templates/index.html](src/templates/index.html) - _Main homepage, contains the hero section & features listed._
    - [templates/dashboard.html](src/templates/dashboard.html) - _User dashboard, containing events list and management options._
    - [templates/checkin.html](src/templates/checkin.html) - _Event page displayed to the user when they scan the QR code to check-in for an event._
    - [templates/manage_event.html](src/templates/manage_event.html) - _Dashboard page / section to change the name of an event, change its open / close status or permanently delete an event._
    - [templates/view_event.html](src/templates/view_event.html) - _Dashboard page / section to view the event QR code and share it. Also, includes a table to view attendees info and options to download the list as a `.csv` file._
    - [templates/settings.html](src/templates/settings.html) - _Contains buttons to permanently delete the user's data or the events created by that particular user._
    - _(Other template files are [templates/login.html](src/templates/login.html), [templates/register.html](src/templates/register.html), etc.)_

### Static Files:

- All the "static" content required by the frontend including `CSS`, `JavaScript` and image files are in the [src/static/](src/static/) directory.
- #### Styles (_CSS_):
    Files are in the [static/css](src/static/css) directory.
    - [css/style.css](src/static/css/style.css) - _Main application CSS styles of the project._
    - [css/dashboard.css](src/static/css/dashboard.css) - _Styling for the user dashboard pages._
- #### Scripts (_JavaScript_):
    The [static/js](src/static/js/) directory contains a single JS file; [js/dashboard.js](src/static/js/dashboard.js) containing the code to convert the time stored in DB to local user time in the browser. This file also contains the code for QR code sharing / downloading and maps the specific functions to various button and other events in the frontend dashboard.
- #### Images:
    The [static/images](src/static/images/) directory contains the images such as the website favicon / logo and other images used in the dashboard.
- #### QR Code Images
    The [static/qrcodes](src/static/qrcodes/) directory is where the generated QR codes of events are stored. _(If its not visible in the repository / folder, running the program for the first time will automatically create it.)_

## DataBase Design:

SmartAttend uses **MySQL** to store its application data.

```mermaid
erDiagram
    direction LR

    ORGANIZERS ||--o{ EVENTS : organizes
    EVENTS ||--o{ ATTENDANCE : records

    ORGANIZERS {
        int id PK
        varchar name "100 characters"
        varchar email UK "254 characters"
        varchar password_hash "255 characters"
    }

    EVENTS {
        int id PK
        varchar title "200 characters"
        varchar qr_token UK "100 characters"
        boolean is_open
        datetime created_at
        int organizer_id FK
    }

    ATTENDANCE {
        int id PK
        varchar attendee_name "100 characters"
        varchar email "254 characters"
        datetime checked_in_at
        int event_id FK
    }
```

The above diagram, generated using [Mermaid](https://mermaid.ai/open-source/), shows the information stored in each table, including the data types, keys (primary & foreign), etc.

There is a **one-to-many** relationship between `Organizers` and `Events` tables, and also with `Events` and `Attendance`.

## Security Considerations

SmartAttend uses password hashing (using `Argon2id` algorithm) rather than storing plaintext passwords.

Session middleware supports organizer authentication, and routes that modify data validate submitted CSRF tokens where implemented.

Event-management operations verify that the authenticated
organizer owns the requested event. Database constraints provide an
additional safeguard against duplicate attendance entries.

Database credentials and session secrets are configured through
environment variables instead of being hard-coded in the source code.

## Use of AI models / agents in Development

**Some well-known AI models / agents like _`ChatGPT`_ and _`Github Copilot`_ were used in some parts of the project and the code was manually reviewed by me properly.**

Some parts of this _README_ file are from an AI agent. But everything is verified and reviewed.

**The parts / lines of code generated by AI is clearly mentioned / marked in in the code files using proper comments.**

While developing this project, I also asked AI about various things like how to handle authentication properly, how to prepare ORM models for the database, how to protect some certain application routes, etc.

I also asked it it review my project from time to time and warn me of any possible security or other errors and helped me fix them.

## Design Decisions

Initially, I wanted to make this application using `Python + FastAPI` as the backend and `HTML, CSS, Vanilla JavaScript` as the frontend but honestly speaking, I was a beginner in JS and didn't know much of the language, like `fetch` method and `Promises`.

So, I thought why not just make the whole application in Python with minimal client-side JS? So, that's why I used the current tech stack.

### Why FastAPI?

I could have used `Flask` as taught in the course but I wanted to try something different and `FastAPI` has a very great choice because of the ease of data validation and automatic API docs.

### Why MySQL as the DataBase?

I am an undergrad in CS _(as of Oct 2026)_, and we were taught `MySQL` in the college. So, I decided to go with that and practice with MySQL.

### Why use ORMs?

One of the seniors in my college told me that using ORMs is very helpful and I can migrate my DB with minimal code changes.

And it helped me very much during the development process. I didn't have to write queries manually, I just need to pass the new objects to the pre-defined `SQLAlchemy ORM` methods and the library would handle it automatically for me and perform many other operations for me with minimal code and fewer function calls.

## Challenges and Future Improvements

During the development, I encountered many challenges and the most challenging for me was the frontend design part, like making the webpage responsive on smaller devices, handling user inputs and button events in the frontend, etc.

On the backend side, I had to be very careful about the access to certain pages and the protection of particular resource, like an event created by an organizer should not be accessible by another organizer.

I had to validate user inputs & verify request headers at each route and it was quite a difficult task for me to manage it.

But, I got to learn a lot of new things while fixing many errors and I enjoyed the process.

**Potential future improvements include attendee analytics, improved
mobile interfaces, email notifications, event scheduling, and additional
attendance verification methods like biometric verification, etc.**

More features can be added like:

- Showing the live data / attendees count in the organizer dashboard using websockets.
- Allowing the event organizer to collect more information from attendees _(like making a custom form in Google Forms)_ instead of the default name and email ID.
- Making event scheduling more smarter, like auto-closing attendee forms at a specific time, etc.

## Acknowledgments

I would like to express my sincere gratitude to **Dr. David J. Malan** and the entire **CS50 team at Harvard University** for creating such an engaging, insightful, and inspiring course.

I am grateful for the knowledge, guidance, and inspiration this course **_(CS50x)_** has provided.

This project is a reflection of what I have learned throughout this journey, and I look forward to continuing to learn, build, and improve as a developer.

Thank you to everyone who makes CS50 possible.
