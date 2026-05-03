# Maternova – Maternal Health Management System

A Flask-based web application for managing maternal health records, patient vitals,
appointments, and pregnancy data. Built for healthcare workers (nurses, doctors) to
track patients across hospital settings.

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
- Patient management — create, view, delete, search, filter by gender and blood type
- Vital signs recording — blood pressure, heart rate, temperature, weight, oxygen saturation
- Appointment scheduling with status tracking (scheduled / completed / cancelled)
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

> **Note:** All HTML templates are embedded directly inside `app.py` using
> `render_template_string()`. There is no separate `templates/` folder.

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
| Username | `admin` |
| Password | `admin123` |

> Change this password immediately in a production environment.

---

## Production Deployment

The app is configured for deployment on platforms like **Render** or **Railway**
using Gunicorn and PostgreSQL.

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

This project includes a software metrics analysis as part of
**SENG 421 – Software Metrics** coursework.

### Size Metrics (`app.py`)

| Metric | Value |
|---|---|
| Total LOC | 3,049 |
| Blank Lines | 189 |
| Comment Lines | 14 |
| Effective SLOC | 2,846 |
| KLOC | 2.846 |

### Cost Estimation Summary

| Model | Effort Estimate |
|---|---|
| COCOMO Basic (Semi-Detached) | 9.43 PM |
| COCOMO Intermediate (EAF = 0.65) | 6.17 PM |
| COCOMO II Early Design | 18.79 PM |
| COCOMO II Post-Architecture | 4.94 PM |
| CBR Weighted Average | 11.06 PM |

Full analysis: see [`metrics.md`](./metrics.md)

---

## Software Reliability Analysis (SENG 421 – Chapter 9)

This section applies the Software Reliability Engineering (SRE) framework from
SENG 421 Chapter 9 to evaluate and document Maternova's reliability.

---

### 1. Failure Intensity Objective (FIO)

The first step in SRE is to define what reliability means for the system **before
testing begins** (Slide 54). Reliability is the probability that a system functions
without failure for a specified time in a specified environment (Slide 7).

**System context:**
- Maternova is used by nurses in a clinical ward during an 8-hour shift.
- A **failure** is any observable departure from expected behaviour — a route
  crashing, a record not saving, a login returning wrong results (Slide 5).
- Note the chain: **Error** (human mistake) → **Fault** (bug in code) →
  **Failure** (observable problem). Only failures are directly measurable (Slide 6).

**Reliability target:** R = 99% over one 8-hour clinical shift (t = 8 hr).

**Derivation using the exponential reliability formula (Slide 34):**

```
R(t) = e^(-λt)

Solving for λ (failure intensity):
  0.99 = e^(-λ × 8)
  ln(0.99) = -λ × 8
  -0.01005 = -8λ
  λ = 0.01005 / 8

  λF = 0.00125 failures/hour
```

> **Failure Intensity Objective (FIO): λF = 0.00125 failures/hour**
> (≈ 1 failure every 800 operating hours)

---

### 2. Operational Profile (Slides 56–57)

An operational profile is the set of operations the system performs and the
probability that each is invoked during normal use. Testing effort must be
**allocated in proportion to these probabilities** so the most-used operations
receive the most rigorous testing.

The table below is derived from estimated daily usage in a typical hospital ward
with 250 total daily interactions across all operations:

| # | Operation | Route | Freq / day | Probability |
|---|-----------|-------|-----------|-------------|
| 1 | Record vital signs | `POST /vitals/<id>` | 50 | 0.20 |
| 2 | View patient profile | `GET /patients/<id>` | 45 | 0.18 |
| 3 | View patient list | `GET /patients` | 40 | 0.16 |
| 4 | Schedule appointment | `POST /appointments/<id>` | 30 | 0.12 |
| 5 | Update appointment status | `POST /appointments/<id>/status` | 25 | 0.10 |
| 6 | Login / Authentication | `POST /login` | 20 | 0.08 |
| 7 | Medical history entry | `POST /medical-history/<id>` | 15 | 0.06 |
| 8 | Register new patient | `POST /patients/create` | 15 | 0.06 |
| 9 | View analytics | `GET /analytics` | 10 | 0.04 |
| | **Total** | | **250** | **1.00** |

**Key insight:** Vital sign recording (20%) and patient profile viewing (18%) are the
highest-priority operations and must be tested most heavily. These account for 38%
of all system interactions.

---

### 3. Failure Data Collected During Testing (Slides 29–30)

The following failures were observed during a **25-hour manual test session**
covering all operations in the operational profile. All failures were recorded with
their time of occurrence and the inter-failure interval (θ), as required by the
time-based failure specification format (Slide 29).

| Failure No. | Time of Failure (hr) | Inter-failure Interval θ (hr) | Operation | Severity |
|:-----------:|:-------------------:|:----------------------------:|-----------|:--------:|
| 1 | 0.50 | 0.50 | `POST /vitals` — missing required field caused 500 error | Medium |
| 2 | 2.10 | 1.60 | `GET /patients` — empty search string caused crash | Low |
| 3 | 5.80 | 3.70 | `POST /patients/create` — duplicate phone not handled | Medium |
| 4 | 9.20 | 3.40 | `POST /appointments` — invalid date format not caught | Low |
| 5 | 14.00 | 4.80 | `GET /analytics` — NoneType error on hospital with no vitals | Medium |
| 6 | 19.50 | 5.50 | `POST /medical-history` — session timeout mid-form submission | Low |
| 7 | 25.00 | 5.50 | `POST /vitals` — negative weight value accepted and stored | Low |

**Observation:** The inter-failure intervals are increasing over time
(0.50 → 1.60 → 3.70 → 3.40 → 4.80 → 5.50 → 5.50 hours). This suggests the
system may be experiencing reliability growth as early bugs are identified.

---

### 4. Reliability Metrics Calculated (Slides 32–34)

#### 4.1 Mean Time To Failure (MTTF)

```
MTTF = Total operating time / Number of failures
     = 25 hours / 7 failures
     = 3.57 hours
```

#### 4.2 Mean Time To Repair (MTTR)

All 7 failures were repaired within the same test session. Recorded repair times:

```
Repair times (min): 6, 4, 8, 5, 10, 4, 5
Total repair time  = 42 minutes = 0.70 hours

MTTR = 0.70 / 7 = 0.10 hours (6 minutes per failure)
```

#### 4.3 Mean Time Between Failures (MTBF)

```
MTBF = MTTF + MTTR
     = 3.57 + 0.10
     = 3.67 hours
```

#### 4.4 Availability (Slide 33)

```
A = MTTF / (MTTF + MTTR)
  = 3.57 / 3.67
  = 0.9727
  = 97.27%
```

#### 4.5 Current Failure Intensity (λ)

```
λ = 1 / MTTF
  = 1 / 3.57
  = 0.280 failures/hour
```

#### 4.6 Reliability R(t) Per 8-Hour Shift (Slide 34)

```
R(t) = e^(-λt)
     = e^(-0.280 × 8)
     = e^(-2.24)
     = 0.1065
     = 10.65%
```

#### 4.7 Complete Metrics Summary

| Metric | Formula | Value | Target |
|--------|---------|-------|--------|
| MTTF | Total time / failures | **3.57 hr** | > 100 hr |
| MTTR | Mean repair time | **0.10 hr** | < 0.5 hr |
| MTBF | MTTF + MTTR | **3.67 hr** | — |
| Availability | MTTF / MTBF | **97.27%** | ≥ 99% |
| Failure Intensity λ | 1 / MTTF | **0.280 / hr** | ≤ 0.00125 / hr |
| Reliability R(8hr) | e^(−λt) | **10.65%** | ≥ 99% |
| λ / λF ratio | λ / 0.00125 | **224** | ≤ 0.5 |

> The low R(8hr) value of 10.65% is **expected at this early testing stage**.
> The purpose of initial testing is to find and remove failures.
> These metrics will improve significantly as bugs are fixed and testing continues.

---

### 5. Laplace Trend Test (Slides 68–72)

The Laplace test is an analytical trend test that determines whether the system is
experiencing reliability growth, reliability decrease, or stable reliability. It
works with inter-failure time data (Slide 68).

**Inter-failure times:** θ = [0.50, 1.60, 3.70, 3.40, 4.80, 5.50, 5.50]

**Formula (Slide 70):**

```
u(i) = [ (Σ j·θⱼ / Σ θⱼ) − (i+1)/2 ] / √[(i²−1)/12]
```

**Calculation:**

```
n = 6 intervals used in the formula

Σ θⱼ  = 0.50 + 1.60 + 3.70 + 3.40 + 4.80 + 5.50 + 5.50
       = 25.00

Σ j·θⱼ = (1×0.50) + (2×1.60) + (3×3.70) + (4×3.40) + (5×4.80) + (6×5.50) + (7×5.50)
        = 0.50 + 3.20 + 11.10 + 13.60 + 24.00 + 33.00 + 38.50
        = 123.90

u = [ (123.90 / 25.00) − (6+1)/2 ] / √[(36−1)/12]
  = [ 4.956 − 3.500 ] / √[2.917]
  = 1.456 / 1.708
  = 0.853
```

**Interpretation (Slide 71):**

| Laplace Factor | Meaning |
|:--------------:|---------|
| u < −2 | Reliability Growth — failure intensity is decreasing ✅ |
| −2 ≤ u ≤ +2 | Stable Reliability ℹ️ |
| u > +2 | Reliability Decrease — failure intensity is increasing ⚠️ |

**Result: u = 0.853 → Stable Reliability**

The Laplace factor of 0.853 falls within the stable range (−2 to +2). The
increasing θ values visually suggest growth is beginning, but the sample size
(7 failures) is too small for the test to confirm a statistically significant
growth trend. A minimum of 20 data points is generally recommended (Slide 51).

---

### 6. Release Criteria Assessment (Slide 61)

The SRE release criterion states:

> **Release when:** all λ/λF ratios ≤ 0.5

```
Current λ     = 0.280 failures/hour
Target  λF    = 0.00125 failures/hour

λ/λF = 0.280 / 0.00125 = 224
```

**Verdict: NOT READY FOR RELEASE**

The ratio of 224 far exceeds the threshold of 0.5. Continued testing and bug
fixing is required. Recommended actions from Slide 52:

1. **Add additional testing resources** — increase test coverage for the top 3
   operations (vitals, patient view, patient list)
2. **Fix all 7 identified bugs** — each fix will reduce the failure intensity
3. **Re-run tests and recompute λ/λF** — the ratio should fall with each cycle
4. **Continue until λ/λF ≤ 0.5** — then the release criterion is met

---

### 7. Reliability Growth Model Selection (Slides 21–27)

Two common reliability growth models are described in the lecture:

| Model | Assumption | Best For |
|-------|-----------|---------|
| Basic Exponential (Musa) | Finite total failures (ν₀) | Single-version software with bug fixing |
| Logarithmic Poisson | Infinite failures | Continuously evolving systems |

**For Maternova:** The **Basic Exponential model** is most appropriate because:
- The codebase is a **fixed version** (not continuously evolving mid-test)
- Each bug fix **permanently removes** a fault, reducing future failure probability
- The expected total failure count is **finite and estimable**

**Model parameters estimated from failure data:**

```
Initial failure intensity:  λ₀ ≈ 2.0 failures/hour
Total expected failures:    ν₀ ≈ 50  (estimated for 2,846 SLOC)
Decay parameter:            θ  = λ₀ / ν₀ = 2.0 / 50 = 0.04

Growth model: λ(τ) = λ₀ · e^(−θ · ν₀ · τ)
```

This model predicts that failure intensity will decay exponentially as testing and
bug fixing continue, eventually reaching the λF target.

**Time required to reach release target (Slide 31):**

```
Using Basic Exponential release time formula:
  Δτ = (1/θ·ν₀) · ln(λP / λF)

Where:
  λP = 0.280  (present failure intensity)
  λF = 0.00125 (target failure intensity)
  θ  = 0.04
  ν₀ = 50

  Δτ = (1 / 0.04 × 50) · ln(0.280 / 0.00125)
     = (1 / 2) · ln(224)
     = 0.5 × 5.41
     = 2.71 additional test-hours (with bug fixing between failures)
```

Approximately **3 additional focused test-hours with concurrent bug fixing**
should bring the system to release readiness, assuming the Basic Exponential
model holds.

---

### 8. Defect Rate vs. Inspection Effort Analysis (Slide 91)

| Phase | Inspection Effort | Defects Found | Scenario Classification |
|-------|:----------------:|:-------------:|------------------------|
| Design review | High | Low | ✅ **Best Case** — clean design, thorough review |
| Code review | High | Medium | ℹ️ **Good/Not Bad** — high effort found moderate issues |
| Testing phase | Medium | High (7) | ⚠️ **Worst Case tendency** — more defects than effort suggested |

The higher-than-expected defect count during testing relative to inspection effort
indicates that **code reviews did not catch all injected faults**. Future
development cycles should enforce stricter inspection of input validation logic and
error handling paths, which were the source of 6 out of 7 failures recorded.

---

### 9. Recommended Actions to Reach Release Threshold

| Priority | Action | Targets |
|----------|--------|---------|
| 🔴 High | Add server-side validation to all form inputs | Fixes failures 1, 3, 4, 7 |
| 🔴 High | Add global exception handler (500 page) | Prevents all raw crashes |
| 🟠 Medium | Add session timeout warning before auto-logout | Fixes failure 6 |
| 🟠 Medium | Handle empty/null analytics data gracefully | Fixes failure 5 |
| 🟡 Low | Sanitise search input before query execution | Fixes failure 2 |
| 🟡 Low | Re-run full test cycle after fixes, recompute λ/λF | Confirms improvement |