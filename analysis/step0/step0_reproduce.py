"""Step 0: reproduce published national figures from HINTS 7 and PIAAC Cycle 2 (U.S.).
Writes step0_results.csv and step0_results.md next to this script."""
import os
import numpy as np
import pandas as pd
import survey_est as se

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []

def add(survey, statistic, published, source, r, universe_note=""):
    rows.append({"survey": survey, "statistic": statistic, "published": published,
                 "reproduced": round(r["est"], 1), "se": round(r["se"], 2),
                 "n": r["n"], "diff": round(r["est"] - published, 1),
                 "source": source, "universe": universe_note})

# ---------------- HINTS 7: weighted percentages in the Public Codebook ----------------
h, hm = se.load_hints()
CB = "HINTS 7 Public Codebook (weighted percent, denominator = all 7,278 incl. missing codes)"
targets = {
    "ConfidentMedForms": {1: 64.1, 2: 23.1, 3: 7.8, 4: 3.2},
    "HealthInsurance2": {1: 90.3, 2: 8.5},
    "GeneralHealth": {1: 10.4, 2: 33.0, 3: 35.7, 4: 14.1, 5: 2.7},
    "EducA": {1: 5.8, 2: 19.9, 3: 35.9, 4: 31.5},
}
labels = {v: hm.value_labels.get(hm.variable_to_label.get(v), {}) for v in targets}
for var, codes in targets.items():
    for code, pub in codes.items():
        r = se.hints_estimate(h, h[var] == code)
        add("HINTS 7", f"{var} = {labels[var].get(code, code)}", pub, CB, r, "all respondents")
# weighted population total check
tot = float(h[se.HINTS_W0].sum())
rows.append({"survey": "HINTS 7", "statistic": "Weighted population total", "published": 262266460,
             "reproduced": round(tot), "se": "", "n": len(h), "diff": round(tot - 262266460),
             "source": "Codebook: sum of weighted sample sizes for HealthInsurance2", "universe": "all respondents"})
# valid-only version of the primary confidence item (what the analysis will use)
valid = h["ConfidentMedForms"] > 0
r = se.hints_estimate(h, h["ConfidentMedForms"] == 1, valid)
rows.append({"survey": "HINTS 7", "statistic": "ConfidentMedForms = Very (valid answers only)", "published": "",
             "reproduced": round(r["est"], 1), "se": round(r["se"], 2), "n": r["n"], "diff": "",
             "source": "no published figure; analysis denominator", "universe": "valid answers"})

# ---------------- PIAAC Cycle 2 U.S.: NCES Highlights of the 2023 U.S. PIAAC Results ----------------
p, pm = se.load_piaac()
NC = "NCES, Highlights of the 2023 U.S. PIAAC Results (nces.ed.gov/surveys/piaac/2023/national_results.asp)"
A = "ages 16-65"
add("PIAAC", "Literacy: Level 1 or below (<226), %", 28, NC, se.piaac_estimate(p, "LIT", "prop", hi=226), A)
add("PIAAC", "Literacy: Level 3 or above (>=276), %", 44, NC, se.piaac_estimate(p, "LIT", "prop", lo=276), A)
add("PIAAC", "Numeracy: Level 1 or below (<226), %", 34, NC, se.piaac_estimate(p, "NUM", "prop", hi=226), A)
add("PIAAC", "Numeracy: Level 3 or above (>=276), %", 38, NC, se.piaac_estimate(p, "NUM", "prop", lo=276), A)
male, female = p["GENDER_R"] == 1, p["GENDER_R"] == 2
add("PIAAC", "Literacy average, men", 257, NC, se.piaac_estimate(p, "LIT", "mean", male), "men 16-65")
add("PIAAC", "Literacy average, women", 260, NC, se.piaac_estimate(p, "LIT", "mean", female), "women 16-65")
add("PIAAC", "Numeracy average, men", 253, NC, se.piaac_estimate(p, "NUM", "mean", male), "men 16-65")
add("PIAAC", "Numeracy average, women", 245, NC, se.piaac_estimate(p, "NUM", "mean", female), "women 16-65")
add("PIAAC", "Literacy L1 or below, men, %", 29, NC, se.piaac_estimate(p, "LIT", "prop", male, hi=226), "men 16-65")
add("PIAAC", "Literacy L1 or below, women, %", 26, NC, se.piaac_estimate(p, "LIT", "prop", female, hi=226), "women 16-65")
add("PIAAC", "Numeracy L1 or below, women, %", 36, NC, se.piaac_estimate(p, "NUM", "prop", female, hi=226), "women 16-65")
# education: NCES groups less than HS / HS / more than HS. Try ISCED 4 with HS and with more-than-HS.
ed = p["EDCAT8_TC1"]
lths, hs_a, more_a = ed <= 2, ed == 3, ed >= 4
hs_b, more_b = ed.isin([3, 4]), ed >= 5
add("PIAAC", "Literacy average, less than high school", 213, NC, se.piaac_estimate(p, "LIT", "mean", lths), "EDCAT8 1-2")
add("PIAAC", "Literacy L1 or below, less than high school, %", 55, NC, se.piaac_estimate(p, "LIT", "prop", lths, hi=226), "EDCAT8 1-2")
add("PIAAC", "Numeracy average, less than high school", 199, NC, se.piaac_estimate(p, "NUM", "mean", lths), "EDCAT8 1-2")
add("PIAAC", "Numeracy L1 or below, less than high school, %", 65, NC, se.piaac_estimate(p, "NUM", "prop", lths, hi=226), "EDCAT8 1-2")
add("PIAAC", "Literacy average, high school (ISCED 3 only)", 246, NC, se.piaac_estimate(p, "LIT", "mean", hs_a), "EDCAT8 3")
add("PIAAC", "Literacy average, high school (ISCED 3+4)", 246, NC, se.piaac_estimate(p, "LIT", "mean", hs_b), "EDCAT8 3-4")
add("PIAAC", "Literacy L1 or below, high school (ISCED 3 only), %", 32, NC, se.piaac_estimate(p, "LIT", "prop", hs_a, hi=226), "EDCAT8 3")
add("PIAAC", "Literacy L1 or below, high school (ISCED 3+4), %", 32, NC, se.piaac_estimate(p, "LIT", "prop", hs_b, hi=226), "EDCAT8 3-4")
add("PIAAC", "Numeracy average, high school (ISCED 3 only)", 232, NC, se.piaac_estimate(p, "NUM", "mean", hs_a), "EDCAT8 3")
add("PIAAC", "Numeracy average, high school (ISCED 3+4)", 232, NC, se.piaac_estimate(p, "NUM", "mean", hs_b), "EDCAT8 3-4")
add("PIAAC", "Literacy average, more than high school (ISCED 4+)", 287, NC, se.piaac_estimate(p, "LIT", "mean", more_a), "EDCAT8 4-8")
add("PIAAC", "Literacy average, more than high school (ISCED 5+)", 287, NC, se.piaac_estimate(p, "LIT", "mean", more_b), "EDCAT8 5-8")
add("PIAAC", "Literacy L1 or below, more than high school (ISCED 4+), %", 13, NC, se.piaac_estimate(p, "LIT", "prop", more_a, hi=226), "EDCAT8 4-8")
add("PIAAC", "Literacy L1 or below, more than high school (ISCED 5+), %", 13, NC, se.piaac_estimate(p, "LIT", "prop", more_b, hi=226), "EDCAT8 5-8")
add("PIAAC", "Numeracy L1 or below, more than high school (ISCED 4+), %", 16, NC, se.piaac_estimate(p, "NUM", "prop", more_a, hi=226), "EDCAT8 4-8")
add("PIAAC", "Numeracy L1 or below, more than high school (ISCED 5+), %", 16, NC, se.piaac_estimate(p, "NUM", "prop", more_b, hi=226), "EDCAT8 5-8")
# extra: full distribution by level (no published target), useful for the site
for name, lo, hi in [("Below Level 1 (<176)", None, 176), ("Level 1 (176-225)", 176, 226), ("Level 2 (226-275)", 226, 276),
                     ("Level 3 (276-325)", 276, 326), ("Level 4/5 (>=326)", 326, None)]:
    r = se.piaac_estimate(p, "LIT", "prop", lo=lo, hi=hi)
    rows.append({"survey": "PIAAC", "statistic": f"Literacy: {name}, %", "published": "", "reproduced": round(r["est"], 1),
                 "se": round(r["se"], 2), "n": r["n"], "diff": "", "source": "no single published target", "universe": A})
r = se.piaac_estimate(p, "LIT", "mean")
rows.append({"survey": "PIAAC", "statistic": "Literacy average, all adults", "published": "", "reproduced": round(r["est"], 1),
             "se": round(r["se"], 2), "n": r["n"], "diff": "", "source": "not on the NCES page fetched", "universe": A})

out = pd.DataFrame(rows)
out.to_csv(os.path.join(HERE, "step0_results.csv"), index=False)
with open(os.path.join(HERE, "step0_results.md"), "w") as f:
    f.write("# Step 0 results: reproduced vs published\n\n")
    f.write("Generated by step0_reproduce.py. `diff` = reproduced − published (percentage points or score points).\n\n")
    f.write(out[["survey", "statistic", "published", "reproduced", "se", "n", "diff", "universe"]].to_markdown(index=False))
    f.write("\n\nSources: " + CB + "; " + NC + ".\n")
print(out[["survey", "statistic", "published", "reproduced", "se", "n", "diff"]].to_string())
