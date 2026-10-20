# Step 0: pipeline validation

Reproduces published national figures from both surveys with the official weights and variance methods, in Python.

- `survey_est.py`: estimation helpers. HINTS 7 jackknife (50 replicates, coefficient 0.98); PIAAC Fay-BRR (U.S.: 44 replicates, k = 0.3) with Rubin combination over the 10 plausible values.
- `step0_reproduce.py`: runs the comparisons and writes `step0_results.csv` and `step0_results.md`.
- Run: `cd analysis/step0 && python3 step0_reproduce.py` (needs pandas, numpy, pyreadstat, tabulate).

Result (2026-10-18): every HINTS 7 codebook percentage reproduces exactly (diff 0.0) and the weighted population total matches (262,266,460). Every NCES 2023 PIAAC figure reproduces within rounding (|diff| ≤ 0.5) once education is grouped the way NCES groups it: "high school" = ISCED 3 + 4 (EDCAT8_TC1 3–4), "more than high school" = ISCED 5 and above (EDCAT8_TC1 5–8).

Published figures without standard errors: NCES publishes none on the results page and the HINTS codebook reports only weighted percentages, so the SEs here are validated by method (documented formulas), not against published SEs. The tiny HINTS SEs on education and insurance reflect weight calibration: HINTS 7 rakes the person weights to control totals for health insurance coverage (C1), cancer diagnosis, age, sex, educational attainment and race (Methodology Report, section 5.4).
