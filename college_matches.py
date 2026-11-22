import pandas as pd


FLORIDA_PROFILE_SOURCE = "https://www.flbog.edu/wp-content/uploads/2025/09/25_26_Matrix_Pager.pdf"
# Fall profiles from the 2025–2026 matrix, keyed by College Scorecard institution ID.
# Each row contains the published weighted GPA, ACT composite, and SAT total ranges.
FLORIDA_PROFILES = {
    132903: ((4.11, 4.57), (28, 32), (1310, 1430)),  # UCF
    133650: ((3.69, 4.25), (22, 27), (1080, 1230)),  # FAMU
    133669: ((3.78, 4.35), (22, 28), (1100, 1280)),  # FAU
    133951: ((4.10, 4.60), (27, 31), (1250, 1390)),  # FIU
    134097: ((4.30, 4.60), (30, 33), (1370, 1460)),  # FSU
    134130: ((4.50, 4.70), (31, 34), (1390, 1510)),  # UF
    136172: ((4.00, 4.53), (22, 28), (1100, 1300)),  # UNF
    137351: ((4.03, 4.55), (27, 31), (1260, 1410)),  # USF
    138354: ((3.58, 4.22), (20, 27), (1020, 1230)),  # UWF
    262129: ((3.70, 4.30), (22, 27), (1060, 1240)),  # New College
    433660: ((3.79, 4.54), (21, 26), (1070, 1240)),  # FGCU
    482936: ((3.48, 3.86), (27, 27), (1206, 1206)),  # Florida Poly
}

TEST_COLUMNS = {"ACT": "ACT midpoint", "SAT": "Average SAT"}
# These fixed scales put each gap in comparable units for the ranking.
TEST_GAP_SCALE = {"ACT": 5, "SAT": 150}
GPA_GAP_SCALE = 0.5


def best_matches(schools, gpa, score_type, score, tuition):
    """Return up to five schools closest to the student's reported benchmarks."""
    if gpa is not None:
        profiles = schools["Institution ID"].map(FLORIDA_PROFILES)
        matches = schools.loc[profiles.notna(), ["School", "City", tuition]].copy()
        if not matches.empty:
            profiles = profiles.loc[matches.index]
            gpa_ranges = profiles.map(lambda profile: profile[0])
            matches["Weighted GPA benchmark"] = gpa_ranges.map(lambda bounds: format_range(bounds, ".2f"))
            matches["_gap"] = gpa_ranges.map(lambda bounds: abs(gpa - sum(bounds) / 2) / GPA_GAP_SCALE)
            if score is not None:
                test_index = 1 if score_type == "ACT" else 2
                test_ranges = profiles.map(lambda profile: profile[test_index])
                matches[f"{score_type} benchmark"] = test_ranges.map(lambda bounds: format_range(bounds, "d"))
                test_gap = test_ranges.map(lambda bounds: abs(score - sum(bounds) / 2) / TEST_GAP_SCALE[score_type])
                matches["_gap"] = (matches["_gap"] + test_gap) / 2
            return top_five(matches, tuition), True

    if score is None:
        return pd.DataFrame(), False

    test_column = TEST_COLUMNS[score_type]
    matches = schools.loc[schools[test_column].notna(), ["School", "City", tuition, test_column]].copy()
    matches["_gap"] = matches[test_column].sub(score).abs()
    return top_five(matches, tuition), False


def format_range(bounds, number_format):
    low, high = bounds
    if low == high:
        return format(low, number_format)
    return f"{low:{number_format}}–{high:{number_format}}"


def top_five(matches, tuition):
    matches["_gap"] = matches["_gap"].round(8)
    return matches.sort_values(["_gap", tuition, "School", "City"]).head(5).drop(columns="_gap")
