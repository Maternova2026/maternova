"""
cost_metrics.py
===============
Software Cost Metrics for Maternova (app.py)
Implements: COCOMO Basic, COCOMO II (Early Design & Post-Architecture),
            Rayleigh-Putnam SLIM model, and Case-Based Reasoning (CBR)

Course: SENG 421 – Software Metrics (Chapter 7)
System: Maternova – Maternal Health Management System
"""

import math

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1 – LOC MEASUREMENT (from existing size metrics)
# These values are from the automated LOC analysis of app.py
# ──────────────────────────────────────────────────────────────────────────────

LOC_METRICS = {
    "total_loc":      2967,
    "blank_lines":     176,
    "comment_lines":    11,  # pure comment lines (# lines)
    "effective_loc":  2780,  # NCLOC: total - blank - comment
    "comment_density": round(11 / 2967, 4),
}

# KLOC = Kilo Lines of Code (used by COCOMO formulas)
KLOC = LOC_METRICS["effective_loc"] / 1000   # 2.780 KLOC


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2 – BASIC COCOMO MODEL (Boehm, 1981)
# E = a × (KLOC)^b        [Person-Months]
# T = c × (E)^d           [Months]
#
# Maternova classification: SEMI-DETACHED
#   - Solo developer, moderate Flask/SQLAlchemy experience
#   - Mix of familiar (Python web) and novel (medical domain) work
#   - No tight hardware/time constraints → not Embedded
#   - Not a simple well-understood app → not purely Organic
# ──────────────────────────────────────────────────────────────────────────────

COCOMO_BASIC_MODES = {
    "organic":       {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
    "semi_detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
    "embedded":      {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32},
}


def cocomo_basic(kloc: float, mode: str = "semi_detached") -> dict:
    """
    Basic COCOMO: Effort and development time as a function of KLOC.

    Args:
        kloc:  Size in Kilo Lines of Code
        mode:  'organic', 'semi_detached', or 'embedded'

    Returns:
        dict with effort (PM), development time (months), avg team size
    """
    params = COCOMO_BASIC_MODES[mode]
    effort = params["a"] * (kloc ** params["b"])          # person-months
    tdev   = params["c"] * (effort ** params["d"])        # months
    team   = effort / tdev                                 # average staff
    return {
        "mode":          mode,
        "kloc":          round(kloc, 3),
        "effort_pm":     round(effort, 2),
        "tdev_months":   round(tdev, 2),
        "avg_team_size": round(team, 2),
    }


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3 – INTERMEDIATE COCOMO (with EAF and 15 Cost Drivers)
# E = a × (KLOC)^b × EAF
# EAF = product of all effort multipliers (EM)
#
# Cost driver ratings for Maternova (justified per system characteristics):
#   RELY = High (1.15)   – medical data, patient records → failure has high cost
#   DATA = Low  (0.94)   – SQLite DB, modest data volume
#   CPLX = Nominal (1.0) – standard CRUD + analytics, no AI inference
#   TIME = Low  (1.0)    – no real-time processing constraints
#   STOR = Low  (1.0)    – lightweight SQLite, no memory pressure
#   VIRT = Low  (0.87)   – stable Python/Flask platform
#   TURN = Low  (0.87)   – fast local dev turnaround
#   ACAP = Nominal (1.0) – competent student/early professional developer
#   AEXP = Low  (1.13)   – limited prior medical-domain app experience
#   PCAP = Nominal (1.0) – solid Python programming capability
#   VEXP = High (0.90)   – good platform (Flask/SQLAlchemy) familiarity
#   LEXP = High (0.95)   – strong Python language experience
#   MODP = High (0.91)   – uses modern practices (ORM, blueprints, hashing)
#   TOOL = High (0.91)   – uses VS Code, Git, Netlify, Flask CLI
#   SCED = Nominal (1.0) – no artificial schedule compression
# ──────────────────────────────────────────────────────────────────────────────

COST_DRIVERS_INTERMEDIATE = {
    # Driver        : (rating label, EM value)
    "RELY":   ("High",    1.15),
    "DATA":   ("Low",     0.94),
    "CPLX":   ("Nominal", 1.00),
    "TIME":   ("Nominal", 1.00),
    "STOR":   ("Nominal", 1.00),
    "VIRT":   ("Low",     0.87),
    "TURN":   ("Low",     0.87),
    "ACAP":   ("Nominal", 1.00),
    "AEXP":   ("Low",     1.13),
    "PCAP":   ("Nominal", 1.00),
    "VEXP":   ("High",    0.90),
    "LEXP":   ("High",    0.95),
    "MODP":   ("High",    0.91),
    "TOOL":   ("High",    0.91),
    "SCED":   ("Nominal", 1.00),
}

COCOMO_INTERMEDIATE_MODES = {
    "organic":       {"a": 3.2, "b": 1.05, "c": 2.5, "d": 0.38},
    "semi_detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
    "embedded":      {"a": 2.8, "b": 1.20, "c": 2.5, "d": 0.32},
}


def compute_eaf(cost_drivers: dict) -> float:
    """Compute Effort Adjustment Factor as product of all EM values."""
    eaf = 1.0
    for _, (_, em) in cost_drivers.items():
        eaf *= em
    return round(eaf, 4)


def cocomo_intermediate(kloc: float, mode: str = "semi_detached") -> dict:
    """
    Intermediate COCOMO: Adds EAF from 15 cost drivers.

    Args:
        kloc: Size in KLOC
        mode: development mode

    Returns:
        dict with effort, tdev, eaf, and per-driver breakdown
    """
    params = COCOMO_INTERMEDIATE_MODES[mode]
    eaf    = compute_eaf(COST_DRIVERS_INTERMEDIATE)
    effort = params["a"] * (kloc ** params["b"]) * eaf
    tdev   = params["c"] * (effort ** params["d"])
    team   = effort / tdev

    return {
        "mode":          mode,
        "kloc":          round(kloc, 3),
        "eaf":           eaf,
        "effort_pm":     round(effort, 2),
        "tdev_months":   round(tdev, 2),
        "avg_team_size": round(team, 2),
        "cost_drivers":  {k: {"rating": v[0], "em": v[1]}
                          for k, v in COST_DRIVERS_INTERMEDIATE.items()},
    }


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4 – COCOMO II: EARLY DESIGN MODEL
# E = 2.45 × KLOC × EAF
# Uses 7 combined cost drivers (combining the 17 Post-Architecture drivers)
#
# Function Point count for Maternova:
#   External Inputs  (EI):  8  → login, register, create patient, record vital,
#                                 schedule appt, save pregnancy, medical history, logout
#   External Outputs (EO):  6  → dashboard, patients list, patient profile,
#                                 analytics report, vitals history, appt history
#   External Inquiries(EQ): 5  → search patients, filter by gender/blood, sort,
#                                 view analytics, view flagged vitals
#   Internal Logical Files (ILF): 6 → User, Patient, VitalSign, Appointment,
#                                      PregnancyRecord, MedicalHistory
#   External Interface Files(EIF): 0 → no external system interfaces
#
# FP weights (unadjusted, average complexity):
#   EI × 4, EO × 5, EQ × 4, ILF × 10, EIF × 7
# ──────────────────────────────────────────────────────────────────────────────

FUNCTION_POINTS = {
    "EI":  {"count": 8,  "weight": 4,  "label": "External Inputs"},
    "EO":  {"count": 6,  "weight": 5,  "label": "External Outputs"},
    "EQ":  {"count": 5,  "weight": 4,  "label": "External Inquiries"},
    "ILF": {"count": 6,  "weight": 10, "label": "Internal Logical Files"},
    "EIF": {"count": 0,  "weight": 7,  "label": "External Interface Files"},
}

# LOC per FP for Python (industry average: ~50 SLOC/FP for Python)
LOC_PER_FP_PYTHON = 50

# Early Design EAF (7 combined drivers for Maternova)
EARLY_DESIGN_EAF = {
    "RCPX": ("High",    1.17),   # Product reliability/complexity – medical CRUD
    "RUSE": ("Nominal", 1.00),   # Required reuse – no reuse requirements
    "PDIF": ("Low",     0.87),   # Platform difficulty – Flask is stable and simple
    "PERS": ("Nominal", 1.00),   # Personnel capability – competent solo developer
    "PREX": ("Low",     1.22),   # Personnel experience – limited medical app history
    "FCIL": ("High",    0.87),   # Facilities – good tooling (VS Code, Git, Netlify)
    "SCED": ("Nominal", 1.00),   # Schedule – no compression
}


def compute_ufc() -> dict:
    """Compute Unadjusted Function Count (UFC) from FP table."""
    total = 0
    breakdown = {}
    for key, val in FUNCTION_POINTS.items():
        points = val["count"] * val["weight"]
        breakdown[key] = {
            "label":   val["label"],
            "count":   val["count"],
            "weight":  val["weight"],
            "points":  points,
        }
        total += points
    return {"breakdown": breakdown, "total_ufc": total}


def cocomo2_early_design() -> dict:
    """
    COCOMO II Early Design Model.
    Converts UFC → KLOC using Python LOC/FP ratio, then applies E = 2.45 × KLOC × EAF.
    """
    ufc_data = compute_ufc()
    ufc      = ufc_data["total_ufc"]
    kloc_fp  = (ufc * LOC_PER_FP_PYTHON) / 1000

    eaf_val  = 1.0
    for _, (_, em) in EARLY_DESIGN_EAF.items():
        eaf_val *= em
    eaf_val = round(eaf_val, 4)

    effort = 2.45 * kloc_fp * eaf_val

    return {
        "ufc":          ufc,
        "ufc_breakdown": ufc_data["breakdown"],
        "loc_per_fp":   LOC_PER_FP_PYTHON,
        "kloc_from_fp": round(kloc_fp, 3),
        "eaf":          eaf_val,
        "eaf_drivers":  {k: {"rating": v[0], "em": v[1]}
                         for k, v in EARLY_DESIGN_EAF.items()},
        "effort_pm":    round(effort, 2),
    }


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 5 – COCOMO II: POST-ARCHITECTURE MODEL
# E = 2.45 × (KLOC)^b × EAF
# b = 0.91 + 0.01 × Σ(SF_i)     where 0.91 ≤ b ≤ 1.23
#
# Scale Factors for Maternova:
#   PREC  = Nominal (3.72) – partially new domain (medical), some Python experience
#   FLEX  = High    (2.03) – some flexibility in requirements during build
#   RESL  = Low     (5.65) – limited upfront architecture/risk resolution
#   TEAM  = VeryHigh(1.10) – solo project, no team coordination overhead
#   PMAT  = Low     (6.24) – early-stage developer, CMM Level ~1-2
#
# 17 Post-Architecture cost drivers (same as COCOMO II spec):
# ──────────────────────────────────────────────────────────────────────────────

SCALE_FACTORS = {
    "PREC": ("Nominal",   3.72),
    "FLEX": ("High",      2.03),
    "RESL": ("Low",       5.65),
    "TEAM": ("VeryHigh",  1.10),
    "PMAT": ("Low",       6.24),
}

POST_ARCH_COST_DRIVERS = {
    # Product
    "RELY": ("High",    1.10),
    "DATA": ("Low",     0.90),
    "CPLX": ("Nominal", 1.00),
    "RUSE": ("Nominal", 1.00),
    "DOCU": ("Nominal", 1.00),
    # Platform
    "TIME": ("Nominal", 1.00),
    "STOR": ("Nominal", 1.00),
    "PVOL": ("Low",     0.87),
    # Personnel
    "ACAP": ("Nominal", 1.00),
    "APEX": ("Low",     1.10),
    "PCAP": ("Nominal", 1.00),
    "PEXP": ("High",    0.91),
    "LTEX": ("High",    0.91),
    "PCON": ("Nominal", 1.00),
    # Project
    "TOOL": ("High",    0.90),
    "SCED": ("Nominal", 1.00),
    "SITE": ("High",    0.93),
}


def cocomo2_post_architecture(kloc: float) -> dict:
    """
    COCOMO II Post-Architecture Model.

    Args:
        kloc: Measured KLOC from actual source code

    Returns:
        dict with scaling exponent b, EAF, effort, and full driver tables
    """
    # Compute scaling exponent b
    sf_sum = sum(v for _, v in SCALE_FACTORS.values())
    b      = round(0.91 + 0.01 * sf_sum, 4)
    b      = max(0.91, min(1.23, b))   # clamp to [0.91, 1.23]

    # Compute EAF from 17 cost drivers
    eaf = 1.0
    for _, (_, em) in POST_ARCH_COST_DRIVERS.items():
        eaf *= em
    eaf = round(eaf, 4)

    effort = 2.45 * (kloc ** b) * eaf

    return {
        "kloc":              round(kloc, 3),
        "scale_factors":     {k: {"rating": v[0], "sf_value": v[1]}
                               for k, v in SCALE_FACTORS.items()},
        "sf_sum":            round(sf_sum, 2),
        "b_exponent":        b,
        "eaf":               eaf,
        "cost_drivers":      {k: {"rating": v[0], "em": v[1]}
                               for k, v in POST_ARCH_COST_DRIVERS.items()},
        "effort_pm":         round(effort, 2),
    }


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6 – RAYLEIGH-PUTNAM SLIM MODEL
# Software equation:  size = C × B^(1/3) × T^(4/3)
# Solving for effort: B = (size / C)^3 / T^4
# Peak effort:        E = 0.3945 × B
# Manpower buildup:   B = D × T^3  (D = manpower acceleration)
#
# Maternova parameters:
#   size = 2780 SLOC (effective LOC)
#   PI   = 13  → C = 13,530  (Systems software, Scientific systems)
#   T    = varied to show schedule vs effort tradeoff
#   D    = 15  (standalone system, no complex cross-system interfaces)
# ──────────────────────────────────────────────────────────────────────────────

# Productivity Index → C lookup (from Putnam table)
PI_TABLE = {
    1: 754,    2: 987,    3: 1220,   4: 1597,   5: 1974,
    6: 2584,   7: 3194,   8: 4181,   9: 5186,  10: 6765,
    11: 8362, 12: 10946, 13: 13530, 14: 17711, 15: 21892,
    16: 28657, 17: 35422, 18: 46368, 19: 57314, 20: 75025,
}

MATERNOVA_PI = 13      # Systems software
MATERNOVA_D  = 15      # Standalone system


def putnam_slim(size_sloc: float, pi: int = MATERNOVA_PI,
                durations_years: list = None) -> dict:
    """
    Rayleigh-Putnam SLIM model.
    Computes total effort B and peak effort E for several delivery times.

    Args:
        size_sloc:        Effective LOC
        pi:               Productivity Index (see PI_TABLE)
        durations_years:  List of T values (years) to evaluate

    Returns:
        dict with C value, PI, and a schedule vs effort table
    """
    if durations_years is None:
        durations_years = [1.0, 1.5, 2.0, 2.5, 3.0]

    C = PI_TABLE.get(pi, 13530)
    results = []

    for T in durations_years:
        try:
            # B = (size / C)^3 / T^4   [staff-years]
            B = ((size_sloc / C) ** 3) / (T ** 4)
            E = 0.3945 * B             # peak effort at delivery
            # manpower buildup check: B_check = D × T^3
            B_check = MATERNOVA_D * (T ** 3)
            results.append({
                "T_years":        T,
                "B_staff_years":  round(B, 3),
                "E_peak_years":   round(E, 3),
                "B_manpower_check": round(B_check, 3),
            })
        except ZeroDivisionError:
            pass

    return {
        "size_sloc": size_sloc,
        "pi":        pi,
        "C":         C,
        "D":         MATERNOVA_D,
        "schedule_effort_table": results,
    }


def putnam_schedule_compression_demo(size_sloc: float = 2780,
                                     pi: int = MATERNOVA_PI) -> dict:
    """
    Demonstrates the schedule compression penalty:
    Reducing T by 50% multiplies effort by ~16× (since B ∝ T^-4).
    """
    C      = PI_TABLE[pi]
    T_base = 2.0
    T_half = T_base * 0.5

    B_base = ((size_sloc / C) ** 3) / (T_base ** 4)
    B_half = ((size_sloc / C) ** 3) / (T_half ** 4)
    ratio  = B_half / B_base if B_base > 0 else float("inf")

    return {
        "T_base_years":     T_base,
        "T_compressed_years": T_half,
        "B_base":           round(B_base, 4),
        "B_compressed":     round(B_half, 4),
        "effort_ratio":     round(ratio, 2),
        "note": (f"Halving the schedule multiplied effort by "
                 f"~{ratio:.1f}× (theory: 1/0.5^4 = 16×)"),
    }


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7 – CASE-BASED REASONING (CBR)
# Maternova is the "new case". Two retrieved projects are used for comparison.
# Adaptation rule: Predicted_Effort = (Maternova_LOC / Retrieved_LOC) × Retrieved_Effort
# Final estimate: weighted average based on similarity scores.
# ──────────────────────────────────────────────────────────────────────────────

CBR_CASES = {
    "new_case": {
        "name":             "Maternova",
        "category":         "Medical Web App",
        "language":         "Python/Flask",
        "team_size":        1,
        "system_size_kloc": round(KLOC, 2),
        "effort_pm":        None,   # to be predicted
    },
    "retrieved_1": {
        "name":             "PatientTrack Pro",
        "category":         "Medical Web App",
        "language":         "Python/Flask",
        "team_size":        2,
        "system_size_kloc": 4.5,
        "effort_pm":        18.0,
        "similarity":       0.88,   # 88% similar
    },
    "retrieved_2": {
        "name":             "ClinicManager",
        "category":         "Healthcare Scheduler",
        "language":         "Python/Django",
        "team_size":        2,
        "system_size_kloc": 3.8,
        "effort_pm":        15.0,
        "similarity":       0.61,   # 61% similar
    },
}


def cbr_predict_effort() -> dict:
    """
    Case-Based Reasoning effort prediction for Maternova.

    Uses three strategies:
      1. Adapted effort from single closest project (retrieved_1)
      2. Simple average of both adapted efforts
      3. Weighted average (by similarity score)
    """
    new_size  = CBR_CASES["new_case"]["system_size_kloc"]
    r1        = CBR_CASES["retrieved_1"]
    r2        = CBR_CASES["retrieved_2"]

    # Adaptation: scale effort by relative size
    adapted_1 = (new_size / r1["system_size_kloc"]) * r1["effort_pm"]
    adapted_2 = (new_size / r2["system_size_kloc"]) * r2["effort_pm"]

    # Strategy 1: closest project only
    effort_strategy1 = adapted_1

    # Strategy 2: simple average
    effort_strategy2 = (adapted_1 + adapted_2) / 2

    # Strategy 3: weighted average by similarity
    w1 = r1["similarity"]
    w2 = r2["similarity"]
    effort_strategy3 = (w1 * adapted_1 + w2 * adapted_2) / (w1 + w2)

    return {
        "new_case":           CBR_CASES["new_case"],
        "retrieved_cases":    [r1, r2],
        "adapted_effort_r1":  round(adapted_1, 2),
        "adapted_effort_r2":  round(adapted_2, 2),
        "strategy_1_single":  round(effort_strategy1, 2),
        "strategy_2_average": round(effort_strategy2, 2),
        "strategy_3_weighted":round(effort_strategy3, 2),
    }


# ──────────────────────────────────────────────────────────────────────────────
# SECTION 8 – FULL REPORT RUNNER
# ──────────────────────────────────────────────────────────────────────────────

def print_separator(title: str = "", width: int = 70):
    if title:
        pad = (width - len(title) - 2) // 2
        print("=" * pad + f" {title} " + "=" * (width - pad - len(title) - 2))
    else:
        print("=" * width)


def run_report():
    print_separator()
    print("  MATERNOVA – SOFTWARE COST METRICS REPORT")
    print("  System: app.py | Course: SENG 421 – Software Metrics Ch.7")
    print_separator()

    # ── LOC Summary ──────────────────────────────────────────────────────────
    print_separator("LOC METRICS (from size analysis)")
    for k, v in LOC_METRICS.items():
        print(f"  {k:<22}: {v}")
    print(f"  {'KLOC (effective)':<22}: {KLOC:.3f}")

    # ── Basic COCOMO ─────────────────────────────────────────────────────────
    print_separator("BASIC COCOMO (Boehm 1981)")
    print("  Mode         | Effort (PM) | Tdev (months) | Avg Team")
    print("  " + "-" * 55)
    for mode in COCOMO_BASIC_MODES:
        r = cocomo_basic(KLOC, mode)
        print(f"  {mode:<14} | {r['effort_pm']:>11.2f} | "
              f"{r['tdev_months']:>13.2f} | {r['avg_team_size']:>8.2f}")
    print()
    print("  ★ Recommended mode for Maternova: SEMI-DETACHED")
    r = cocomo_basic(KLOC, "semi_detached")
    print(f"    Effort = {r['effort_pm']} PM  |  Tdev = {r['tdev_months']} months"
          f"  |  Avg Team = {r['avg_team_size']} persons")

    # ── Intermediate COCOMO ───────────────────────────────────────────────────
    print_separator("INTERMEDIATE COCOMO (with 15 Cost Drivers)")
    ic = cocomo_intermediate(KLOC, "semi_detached")
    print(f"  EAF (product of all EMs) : {ic['eaf']}")
    print(f"  Adjusted Effort          : {ic['effort_pm']} PM")
    print(f"  Development Time         : {ic['tdev_months']} months")
    print(f"  Average Team Size        : {ic['avg_team_size']} persons")
    print()
    print("  Cost Driver Breakdown:")
    print(f"  {'Driver':<6} {'Rating':<12} {'EM':>6}")
    print("  " + "-" * 28)
    for driver, info in ic["cost_drivers"].items():
        print(f"  {driver:<6} {info['rating']:<12} {info['em']:>6.2f}")

    # ── COCOMO II Early Design ────────────────────────────────────────────────
    print_separator("COCOMO II – EARLY DESIGN MODEL")
    ed = cocomo2_early_design()
    print("  Function Point Count:")
    print(f"  {'Type':<6} {'Label':<30} {'Count':>5} × {'Wt':>3} = {'Pts':>5}")
    print("  " + "-" * 55)
    for key, val in ed["ufc_breakdown"].items():
        print(f"  {key:<6} {val['label']:<30} {val['count']:>5}   "
              f"{val['weight']:>3}   {val['points']:>5}")
    print(f"  {'':6} {'TOTAL UFC':30} {'':>5}   {'':>3}   {ed['ufc']:>5}")
    print()
    print(f"  LOC per FP (Python avg) : {ed['loc_per_fp']} SLOC/FP")
    print(f"  Derived KLOC from FP    : {ed['kloc_from_fp']}")
    print(f"  EAF (7 combined drivers): {ed['eaf']}")
    print(f"  Effort (E=2.45×KLOC×EAF): {ed['effort_pm']} PM")

    # ── COCOMO II Post-Architecture ───────────────────────────────────────────
    print_separator("COCOMO II – POST-ARCHITECTURE MODEL")
    pa = cocomo2_post_architecture(KLOC)
    print("  Scale Factors:")
    print(f"  {'SF':<6} {'Rating':<12} {'Value':>7}")
    print("  " + "-" * 28)
    for sf, info in pa["scale_factors"].items():
        print(f"  {sf:<6} {info['rating']:<12} {info['sf_value']:>7.2f}")
    print(f"  {'Σ SF':<6} {'':12} {pa['sf_sum']:>7.2f}")
    print(f"  Scaling exponent b = 0.91 + 0.01 × {pa['sf_sum']} = {pa['b_exponent']}")
    print()
    print(f"  EAF (17 cost drivers)   : {pa['eaf']}")
    print(f"  Effort (2.45×KLOC^b×EAF): {pa['effort_pm']} PM")

    # ── Putnam SLIM ───────────────────────────────────────────────────────────
    print_separator("RAYLEIGH-PUTNAM SLIM MODEL")
    slim = putnam_slim(LOC_METRICS["effective_loc"])
    print(f"  Size (SLOC) = {slim['size_sloc']}")
    print(f"  PI = {slim['pi']}  →  C = {slim['C']}  (Systems software)")
    print(f"  D  = {slim['D']}  (standalone system)")
    print()
    print(f"  {'T (yrs)':<10} {'B (staff-yrs)':<16} {'E_peak (yrs)':<16} {'B_manpower'}")
    print("  " + "-" * 60)
    for row in slim["schedule_effort_table"]:
        print(f"  {row['T_years']:<10.1f} {row['B_staff_years']:<16.4f} "
              f"{row['E_peak_years']:<16.4f} {row['B_manpower_check']:.3f}")
    print()
    comp = putnam_schedule_compression_demo()
    print("  Schedule Compression Demo:")
    print(f"  {comp['note']}")

    # ── Case-Based Reasoning ──────────────────────────────────────────────────
    print_separator("CASE-BASED REASONING (CBR)")
    cbr = cbr_predict_effort()
    print("  Attributes        New Case          Retrieved 1        Retrieved 2")
    print("  " + "-" * 70)
    attrs = ["name", "category", "language", "team_size", "system_size_kloc"]
    for a in attrs:
        nc = str(cbr["new_case"].get(a, "?"))
        r1 = str(cbr["retrieved_cases"][0].get(a, "?"))
        r2 = str(cbr["retrieved_cases"][1].get(a, "?"))
        print(f"  {a:<18} {nc:<18} {r1:<18} {r2}")
    print()
    print(f"  Similarity                            "
          f"{cbr['retrieved_cases'][0]['similarity']*100:.0f}%               "
          f"{cbr['retrieved_cases'][1]['similarity']*100:.0f}%")
    print()
    print("  Effort Predictions:")
    print(f"    Strategy 1 (closest project only) : {cbr['strategy_1_single']:.2f} PM")
    print(f"    Strategy 2 (simple average)        : {cbr['strategy_2_average']:.2f} PM")
    print(f"    Strategy 3 (weighted by similarity): {cbr['strategy_3_weighted']:.2f} PM")

    # ── Summary ───────────────────────────────────────────────────────────────
    print_separator("SUMMARY – EFFORT ESTIMATES COMPARISON")
    ic_r  = cocomo_intermediate(KLOC, "semi_detached")
    pa_r  = cocomo2_post_architecture(KLOC)
    ed_r  = cocomo2_early_design()
    cbr_r = cbr_predict_effort()
    slim_r = putnam_slim(LOC_METRICS["effective_loc"])

    estimates = [
        ("COCOMO Basic (semi-detached)",          cocomo_basic(KLOC, "semi_detached")["effort_pm"]),
        ("COCOMO Intermediate (semi-detached)",   ic_r["effort_pm"]),
        ("COCOMO II Early Design",                ed_r["effort_pm"]),
        ("COCOMO II Post-Architecture",           pa_r["effort_pm"]),
        ("CBR Weighted Average",                  cbr_r["strategy_3_weighted"]),
        ("SLIM (T=2.0 yrs)",                      round(slim_r["schedule_effort_table"][2]["B_staff_years"] * 12, 2)),
    ]
    print(f"  {'Model':<42} {'Effort (PM)':>12}")
    print("  " + "-" * 56)
    for name, est in estimates:
        print(f"  {name:<42} {est:>12.2f}")
    print_separator()
    print("  NOTE: All estimates are approximate. COCOMO models are most")
    print("  accurate for systems in the KLOC range they were calibrated on.")
    print("  For a ~2.78 KLOC system, CBR and SLIM may overestimate.")
    print_separator()


if __name__ == "__main__":
    run_report()
