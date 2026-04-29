# Maternova – Maternal Health Management System

A Flask-based web application for managing maternal health records, patient vitals, appointments, and pregnancy data.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| ORM | SQLAlchemy |
| Database | SQLite |
| Auth | Flask-Login, Werkzeug password hashing |
| Frontend | Jinja2 templates, HTML/CSS |
| Deployment | Netlify (via static export) / local Flask server |

---

## Features

- User authentication (register, login, logout)
- Patient management (create, view, search, filter)
- Vital signs recording and history tracking
- Appointment scheduling
- Pregnancy record management
- Medical history logging
- Analytics dashboard with flagged vitals

---

## Project Structure

```
├── app.py                  # Main Flask application (routes, models, logic)
├── cost_metrics.py         # Software cost estimation models (SENG 421 Ch.7)
├── metrics.md              # Software metrics documentation (LOC, Halstead, Cost)
├── README.md               # This file
└── templates/              # Jinja2 HTML templates
```

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/muhumuza684/maternova.git
cd maternova
```

**2. Install dependencies**
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

**3. Run the application**
```bash
python app.py
```

**4. Open in browser**
```
http://127.0.0.1:5000
```

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
| COCOMO Intermediate (EAF=0.65) | 6.17 PM |
| COCOMO II Early Design | 18.79 PM |
| COCOMO II Post-Architecture | 4.94 PM |
| CBR Weighted Average | 11.06 PM |

Full analysis: see [`metrics.md`](./metrics.md)

**Run the cost metrics report:**
```bash
python cost_metrics.py
```


## License

This project is for academic and portfolio purposes.
