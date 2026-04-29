# Maternova – Maternal Health Management System

A Flask-based web application for managing maternal health records, patient vitals, appointments, and pregnancy data. Built for healthcare workers (nurses, doctors) to track patients across hospital settings.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask 2.3.3 |
| ORM | Flask-SQLAlchemy 3.1.1 |
| Auth | Flask-Login 0.6.2, Werkzeug 2.3.7 |
| Database (local) | SQLite |
| Database (production) | PostgreSQL (via psycopg2) |
| Production Server | Gunicorn 21.2.0 |
| Templates | Jinja2 (inline via `render_template_string`) |

---

## Features

- User registration and authentication (nurse / admin roles)
- Patient management — create, view, search, filter by gender and blood type
- Vital signs recording — blood pressure, heart rate, temperature, weight, oxygen saturation
- Appointment scheduling with status tracking
- Pregnancy record management (gravida, para, LMP, EDD, gestational weeks, risk level)
- Medical history logging with conditions, treatments, and medications
- Analytics dashboard with flagged vitals and hospital-level statistics
- Hospital-scoped data — each user only sees patients from their hospital

---

## Project Structure

```
maternova/
├── app.py                  # Entire application — models, routes, and HTML templates
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes venv/, instance/, .env, __pycache__
├── instance/               # Auto-created on first run (not committed)
│   └── maternova.db        # SQLite database (local development only)
├── services/               # Reserved for future service modules
├── uploads/                # Reserved for future file uploads
└── venv/                   # Virtual environment (not committed)
```

> **Note:** All HTML templates are embedded directly inside `app.py` using `render_template_string()`. There is no separate `templates/` folder.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/muhumuza684/maternova.git
cd maternova
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file or export variables directly:

```bash
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=sqlite:///maternova.db   # local
# For production PostgreSQL:
# export DATABASE_URL=postgresql://user:password@host/dbname
```

### 5. Run the application

```bash
python app.py
```

Visit: `http://127.0.0.1:5000`

---

## Default Admin Account

On first run the database is created automatically. Use these credentials to log in:

| Field | Value |
|---|---|
| Email | `admin@maternova.com` |
| Password | `admin123` |

> Change this password immediately in a production environment.

---

## Production Deployment

The app is configured for deployment on platforms like **Render** or **Railway** using Gunicorn and PostgreSQL.

```bash
gunicorn app:app
```

Ensure the following environment variables are set on your platform:

| Variable | Description |
|---|---|
| `SECRET_KEY` | A strong random secret key |
| `DATABASE_URL` | PostgreSQL connection string |
| `PORT` | Port to bind (auto-set by most platforms) |

---

## Software Metrics

This project includes a software metrics analysis module as part of **SENG 421 – Software Metrics** coursework.

### Size Metrics (`app.py`)

| Metric | Value |
|---|---|
| Total LOC | 2,967 |
| Blank Lines | 176 |
| Comment Lines | 11 |
| Effective SLOC | 2,780 |
| KLOC | 2.780 |

### Cost Estimation Summary

| Model | Effort Estimate |
|---|---|
| COCOMO Basic (Semi-Detached) | 9.43 PM |
| COCOMO Intermediate (EAF = 0.65) | 6.17 PM |
| COCOMO II Early Design | 18.79 PM |
| COCOMO II Post-Architecture | 4.94 PM |
| CBR Weighted Average | 11.06 PM |

Full analysis: see [`metrics.md`](./metrics.md)

**Run the cost metrics report:**
```bash
python cost_metrics.py
```

---



## License

This project is for academic and portfolio purposes.
