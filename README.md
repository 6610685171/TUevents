# TUEvents – Thammasat University Event Management Web Site 🎓

**TUevents** is a university web site built to centralize events, announcements, and Lost & Found posts for Thammasat University students, improving accessibility and engagement.

🌐 **Live Demo:** [https://tuevents.pythonanywhere.com/](https://tuevents.pythonanywhere.com/)

**Demo Credentials:**

- Username: 6601888888
- Password: test8888

⚡ **Note:** This repository contains a cleaned-up version of the project focusing on **backend development**, which was my contribution to the original group project.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [My Contributions](#-my-contributions-applied--internship-focused)
- [Key Features](#-key-features)
- [Technologies & Skills](#-technologies--skills)
- [Branches / Versions](#branches--versions)
- [Getting Started](#-getting-started)

---

## 🌿 Project Overview

- **Framework:** Django
- **Database:** SQLite
- **Goal:** Improve accessibility and engagement for Thammasat University students by centralizing campus events, announcements, and Lost & Found posts in a single, easy-to-use platform.

---

## 💼 My Contributions

During the TUEvents project, I was responsible for:

- **Backend Development:** Implemented all backend functionality across multiple iterations, including data handling, user authentication, and feature logic.
- **Frontend Improvements:** Enhanced UI/UX by updating fonts, layouts, and overall website design to make it more user-friendly and modern.
- **Project Planning & Management:** Proposed the project topic, defined project scope, created User Stories, and managed tasks in Jira.
- **Reporting & Documentation:** Organized and formatted the project report, wrote goals, descriptions, and updated content throughout the project.
- **Presentation & Demos:** Created slides for presentations, recorded demo videos for features, and showcased project progress.
- **Testing & Issue Resolution:** Identified and fixed frontend and backend issues, ensuring smooth functionality of the website.
- **Team Coordination:** Reviewed overall project quality and guided improvements in User Stories according to SMART principles.

---

## ⚡ Key Features

### 🔹 Admin Features

- **Add Event:** Create new events by entering event name, description, images, categories, start/end dates, and location.
- **Manage Posts:** View, edit, or delete posts to ensure content is accurate and up-to-date.
- **User Management:** View user information, add new user accounts, and enter student data into the system.
- **View Interested Users:** See the list of users who marked interest in each event and the total number of interested users.

### 🔹 User Features

- **Authentication:** Log in and log out to access features and personal information.
- **Lost & Found:**
  - Post lost items.
  - Post found items to help find their owners.
  - Edit or delete your own posts.
  - Update item status from LOST → FOUNDED.
  - View your own lost & found post history.
- **Event & Club Interaction:**
  - Browse university events and posts from various clubs.
  - Mark favorite events (My Favorite Events).
  - View your own post history in clubs (My Club Post History).
- **Profile Management:** View and update personal information, including name, email, student ID, and profile picture.

### 🔹 Club Member Features

- **Club Announcements:** Post announcements about events or member recruitment, including title, description, start/end dates, images, category, and location.
- **View Club Posts:** Browse announcements from your own club and other university clubs.

---

## 🛠️ Technologies & Skills

- **Languages / Frameworks:** Python, Django, HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite
- **Tools / Tech:** Git, GitHub, Jira, VSCode, Google Workspace, Canva
- **Soft Skills:** Teamwork, Accountability, Attention to detail, Project Management, Documentation

---

## 🌿 Branches / Versions

| Branch                | Description                                            |
| --------------------- | ------------------------------------------------------ |
| **main**              | My version: Clean code, new structure, easier to read  |
| **backup_my_version** | Back up of my_version (main)                           |
| **group-version**     | Original group project version: for reference purposes |

---

## ⚡ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/6610685171/TUevents.git
cd TUevents/webapp
```

### 2. Create a virtual environment & install dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

# Install required packages
pip install -r requirements.txt
💡 Note: Make sure pip is up to date:
```

```bash
pip install --upgrade pip
```

### 3. Apply migrations & run the development server

```bash
python manage.py migrate
python manage.py runserver
```

### 4. Open the app in your browser

Go to http://127.0.0.1:8000 to explore the app.

## 🛠 Tips & Notes

If you encounter errors with ImageField, make sure Pillow is installed:

```bash
pip install Pillow
For views that require login, use the @login_required decorator:
```

```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def my_account(request):
    ...
```

In VS Code, select the project’s virtual environment by pressing Cmd+Shift+P → Python: Select Interpreter → choose /usr/local/bin/python3

---

Thank you for checking out my project! 😊  
Check out the demo and have fun exploring the features!
