# Task Management Web Application 

## Project Overview

This project is a web-based task management application that allows users to:
- Register and login securely
- Create, view, edit, and delete tasks
- Filter tasks by status and priority
- Export tasks to CSV
- Receive email notifications for upcoming deadlines

---

## Technology Stack

**Backend:**
- Python 3.x
- Flask 3.1.2 (Web framework)
- Flask-SQLAlchemy 3.1.1 (ORM)
- Flask-Login 0.6.3 (Session management)
- Flask-WTF 1.2.2 (Form handling)

**Database:**
- SQLite (Lightweight, file-based database)

**Frontend:**
- HTML5
- Tailwind CSS (via CDN)
- JavaScript (for interactivity)

**Testing:**
- pytest 8.4.2

**Additional:**
- APScheduler 3.10.4 (Background tasks)
- python-dotenv 1.2.1 (Environment variables)
- Werkzeug 3.1.3 (Password hashing)

---

## Step 1: Project Setup

### 1.1 Create Project Directory

```
mkdir flask_task_app
cd flask_task_app

```

### 1.2 Set Up Virtual Environment

```
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```
### 1.3 Download repo

```
git clone https://github.com/tsvetkovivan365-code/flask_task_app.git

```

Install:
```
pip install -r requirements.txt

```

### 1.4 Project Structure

```
flask_task_app/
├── app.py                  # Main application file
├── database.py             # Database models
├── forms.py                # WTForms definitions
├── init_db.py              # Database initialization
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (create this)
├── templates/              # HTML templates
│   ├── navbar.html        # Base template with navigation
│   ├── home.html          # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Task dashboard
│   ├── create_task.html   # Create task form
│   └── edit_task.html     # Edit task form
├── static/                 # Static files (optional)
│   └── schedule.svg       # Icon for home page
└── tests/                  # Unit tests
    ├── __init__.py
    └── test_app.py
```

---

## Step 2: Running the Application

### 2.1 Initialize Database

```
python init_db.py

```

Output: `Database tables created successfully!`

---

### 2 Start Flask Application

```
python app.py

```

Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000

```

### 2.1 Access Application

Open browser and navigate to: `http://127.0.0.1:5000`

### 2.2 Create First User

1. Click "Login / Register"
2. Fill out registration form
3. Login with credentials
4. Start creating tasks!


### 3 Run Tests

```
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_app.py::TaskManagementTestCase::test_user_registration_valid
```