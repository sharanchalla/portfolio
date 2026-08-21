# Sharan's Portfolio Web Application

A premium, modern portfolio web application with a responsive user interface, custom light/dark theme system, scroll animations, database backing, and contact submission routing.

## Technology Stack
*   **Backend:** Python 3, Flask, Flask-SQLAlchemy (SQLite)
*   **Frontend:** Semantic HTML5, Vanilla CSS3 (Custom design system with HSL variables), Vanilla Javascript (ES6)
*   **Environment:** Python-dotenv

---

## File Structure

The project has the exact structure shown in the layout specification:

```text
portfolio/
├── css/
│   ├── style.css          # Core layouts, variables, dark/light theme tokens
│   ├── responsive.css     # Navigation drawer, mobile viewports
│   └── animations.css     # Staggered entry transitions, hover lifts
├── js/
│   ├── script.js          # Forms AJAX, navigation, scroll bar triggers
│   └── theme.js           # Theme loader preventing screen flashing
├── models/
│   └── models.py          # SQLAlchemy models (Project, Skill, Certificate, Message)
├── routes/
│   ├── home.py            # Main endpoints (/, /about, /skills, /certificates)
│   ├── project.py         # Catalog listings and projects JSON API
│   └── contact.py         # Contact form POST routes
├── database/
│   └── portfolio.db       # Generated SQLite database file
├── index.html             # Landing template
├── about.html             # Experience timeline template
├── projects.html          # Interactive search / catalog filter template
├── skills.html            # Progress rating metrics template
├── certificates.html      # Licenses template
├── contact.html           # Feedback form layout
├── app.py                 # Application bootstrapper and database seeder
├── config.py              # Variable loader config class
├── requirements.txt       # Project python dependencies
├── .env                   # Environment configurations
└── .gitignore             # Development logs and cache exclusion lists
```

---

## Installation & Setup

Follow these steps to run the application on your computer:

### 1. Prerequisite: Python
Make sure you have Python (version 3.8 or higher) installed. You can verify this by running:
```powershell
python --version
```

### 2. Install Dependencies
Open your terminal (PowerShell, Command Prompt, or Bash), navigate to this portfolio directory, and run the following command to install the required libraries:
```powershell
pip install -r requirements.txt
```

### 3. Start the Flask Server
Run the Flask application by executing the Python startup script:
```powershell
python app.py
```

### 4. Open in Browser
Once running, the terminal will indicate that the server is live. Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## Key Features

1.  **Zero Flashing Theme Engine:** The site uses `js/theme.js` loaded inside the HTML `<head>` tag to read theme settings from `localStorage` and paint the document immediately, preventing dark-to-light theme flashing on page loads.
2.  **Seeded SQLite Database:** Upon starting `app.py` for the first time, a database is created at `database/portfolio.db` and seeded with default skill nodes, certification rows, and projects.
3.  **Real-Time Catalog Search:** The `projects.html` catalog features instantaneous, real-time client-side search and category filtering matching titles and tech tags.
4.  **AJAX Contact Box:** Submitting the form on `contact.html` posts JSON data to the backend via `fetch()`, saves the message inside SQLite, and shows a custom non-blocking Toast alert.
