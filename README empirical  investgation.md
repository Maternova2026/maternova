# Empirical Software Engineering Investigation

A static code analysis tool that applies the **SENG 421 – Chapter 4 Empirical Investigation Framework** to measure internal product attributes of a Python source file.

Built as a companion to `software_size.py`, this tool extends the investigation with Cyclomatic Complexity, derived Halstead metrics (Volume, Difficulty, Effort), formal hypothesis testing, descriptive statistics, and a structured six-phase report.

---

## Project Structure

```
├── app.py                      # Target Flask application (Maternova)
├── software_size.py            # Original LOC + basic Halstead analyzer
├── empirical_investigation.py  # Full empirical investigation (this tool)
├── requirements.txt            # Flask app dependencies
└── README.md                   # This file
```

## What It Measures

### Lines of Code (LOC)

| Metric | Description |
|--------|-------------|
| Total LOC | All lines in the file |
| Blank Lines | Empty lines (`line.strip() == ""`) |
| Comment Lines (CLOC) | Lines containing `#` (includes inline comments) |
| Effective LOC (NCLOC) | Total − Blank − Pure-comment lines |
| Comment Density | CLOC / Total LOC |

### Halstead Metrics

| Symbol | Metric | Formula |
|--------|--------|---------|
| μ1 | Distinct Operators | count of unique OP tokens |
| μ2 | Distinct Operands | count of unique NAME/NUMBER/STRING tokens |
| N1 | Total Operators | all OP token occurrences |
| N2 | Total Operands | all NAME/NUMBER/STRING occurrences |
| μ | Vocabulary | μ1 + μ2 |
| N | Length | N1 + N2 |
| V | Volume | N × log₂(μ) |
| D | Difficulty | (μ1 / 2) × (N2 / μ2) |
| E | Effort | D × V |

### Cyclomatic Complexity (CC)

McCabe's metric per function/method — counts decision points:
`if`, `elif`, `for`, `while`, `except`, `with`, `assert`, `and`, `or`

**Risk bands (SEI standard):**

| CC Range | Risk Level |
|----------|------------|
| 1 – 10 | ✔ Low |
| 11 – 20 | ⚠ Moderate |
| 21 – 50 | ✘ High |
| > 50 | ✘✘ Very High |

---

## Investigation Framework (SENG 421 Chapter 4)

The tool implements all six phases of the empirical research guidelines:

### 1. Experimental Context
Three pre-stated hypotheses (defined before any data is collected):

- **H1** — Comment density < 0.20 → insufficient inline documentation
- **H2** — Halstead Difficulty > 30 → high cognitive effort required
- **H3** — At least one function has CC > 10 → high-risk maintenance area

### 2. Experimental Design
- **Independent variables:** source file, programming language
- **Dependent variables:** LOC, Halstead, and CC metrics
- **Technique:** Third-Degree Contact — static analysis of a source code artifact

### 3. Data Collection
- `EmpiricalDataCollector` — extracts all metrics using Python's `tokenize` and `ast` modules
- Error handling ensures completeness even on malformed tokens (DC2)

### 4. Analysis
- `EmpiricalAnalyzer` — tests each hypothesis against industry baselines
- Descriptive statistics (mean, median, std dev, min, max) for CC distribution

### 5. Presentation
- Raw metric tables with ASCII bar charts
- CC per-function table sorted by complexity
- ASCII histogram of CC distribution

### 6. Interpretation
- Distinguishes statistical vs practical significance (I2)
- Scopes the population the results apply to (I1)
- Explicitly states limitations of the measurement approach (I3)

---

## How to Run

```bash
# Analyse app.py (default)
python empirical_investigation.py

# Analyse any other Python file
python empirical_investigation.py path/to/your_file.py
```

No external dependencies — uses only Python standard library (`tokenize`, `ast`, `re`, `math`).

---

## Sample Output (app.py)


  EMPIRICAL SOFTWARE ENGINEERING INVESTIGATION
  Based on SENG 421 – Chapter 4 Framework


  [DC] LOC METRICS
  Total LOC                      2967
  Blank Lines                     176
  Comment Lines (CLOC)            191
  Effective LOC (NCLOC)          2780
  Comment Density : 0.0644  (recommended ≥ 0.20)

  [DC] HALSTEAD METRICS
  Volume      (V)        31173.75
  Difficulty  (D)           50.77
  Effort      (E)      1582691.29

  [DC] CYCLOMATIC COMPLEXITY (Top 5)
  analytics         CC=19  ⚠ Moderate
  vitals            CC=10  ✔ Low
  login             CC= 6  ✔ Low
  register          CC= 6  ✔ Low
  pregnancy         CC= 6  ✔ Low

  [A] HYPOTHESIS TESTING
  H1  SUPPORTED — density (0.0644) is below threshold (0.20)
  H2  SUPPORTED — difficulty (50.77) exceeds threshold (30)
  H3  SUPPORTED — 1 function(s) exceed the CC threshold
                  Top offender: analytics
```

---

## Key Findings (app.py — Maternova Flask App)

| Hypothesis | Result | Practical Implication |
|------------|--------|-----------------------|
| H1 Comment Density | **SUPPORTED** (0.064 < 0.20) | Developers may struggle with undocumented sections |
| H2 Halstead Difficulty | **SUPPORTED** (50.77 > 30) | High cognitive effort required to modify the codebase |
| H3 Cyclomatic Complexity | **SUPPORTED** (1 function > CC 10) | `analytics` function is a prime refactoring candidate |

---

## Limitations

- Comment detection counts lines with `#`; triple-quoted docstrings are **not** counted as comments
- Cyclomatic Complexity uses regex approximation; a full control-flow graph would be more precise
- Halstead token classification may be affected by decorators and comprehensions
- Results are for a single file at a single point in time — not generalisable without replication

---

 Future Improvements

1. Extend analysis to multiple files (multi-module investigation)
2. Add docstring coverage metric using triple-quoted string detection
3. Implement full control-flow graph for precise Cyclomatic Complexity
4. Integrate results into the Flask dashboard as a `/metrics` route
5. Add fan-in / fan-out coupling metrics
6. Support longitudinal tracking across git commits
7. Visualise results using `matplotlib` or `plotly`

---

Tools Used

- **Python** — standard library only
- `tokenize` — lexical analysis for Halstead metrics
- `ast` — abstract syntax tree for Cyclomatic Complexity and structural counts
- `re` — pattern matching for decision-point detection

---


