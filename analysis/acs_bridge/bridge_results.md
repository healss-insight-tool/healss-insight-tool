# ACS 2024 bridge: literacy and confidence profiles of Medicaid enrollees

Run 2026-10-20 on the archived files (`data/raw/acs2024_pums/acs2024_pus_slim.csv.gz`, `data/raw/piaac_c2_us/PRGUSAP2.sav`, `data/raw/hints7/.../hints7_public.dta`). Code: `build_cells.py` then `bridge.py` in this folder. Full numbers in `bridge_results.csv`; cell compositions in `composition.csv`.

**Status: exploratory, disclosed pre-registration pilot.** These estimates were computed on 2026-10-20, before the OSF registration (https://osf.io/ceztj) was submitted and approved the same day. The registration discloses this run as a pilot seen by Tyler L. Jones only; the numbers are reported as exploratory (E1) and carry no confirmatory weight.

## What the bridge does

Neither public survey identifies Medicaid enrollees. The ACS does (HINS4: "Medicaid, Medical Assistance, or any kind of government-assistance plan for those with low incomes or a disability"), and it shares education, age and sex with both surveys. So:

1. Split adults 20–65 into cells of education × age band (20–34, 35–49, 50–65) × sex. PIAAC uses NCES's three education groups (no diploma; HS/GED/some college no degree/certificate; associate or higher), matched exactly to ACS SCHL 1–15 / 16–19 / 20–24. HINTS uses its own four (`EducA`), matched to SCHL 1–15 / 16–17 / 18–20 / 21–24.
2. Estimate the outcome in each cell from the survey (PIAAC: ten plausible values × 44 Fay-BRR replicates; HINTS: 50 jackknife replicates).
3. Take each coverage group's cell composition from the ACS (2024 1-year PUMS, 1,933,370 person records aged 20–65, 80 successive-difference replicate weights).
4. Combine: estimate = Σ (ACS share of group in cell) × (survey estimate for cell). Standard errors add the ACS and survey replicate variances, which are independent.

**The assumption, stated plainly:** within a cell, Medicaid enrollees are taken to have the same literacy (or confidence) as all adults in that cell. Anything that lowers literacy for Medicaid enrollees beyond their education, age and sex (disability, limited English, poverty) is not captured. The literacy estimate for Medicaid is therefore best read as a **floor**: the true share at or below Level 1 is unlikely to be lower.

## Results (adults 20–65)

| Coverage group (ACS 2024) | No HS diploma, % | Associate or higher, % | Literacy at or below Level 1, % (SE) | Literacy below Level 3, % (SE) | Mean literacy (SE) | "Very confident" filling out medical forms, % (SE) | Very or somewhat confident, % (SE) |
|---|---|---|---|---|---|---|---|
| Medicaid (HINS4 = yes) | 19.5 | 21.5 | **36.0 (1.3)** | 65.8 (1.3) | 243 (1.7) | **59.7 (1.5)** | 84.9 (1.2) |
| Medicaid, excluding dual Medicare | 19.1 | 22.1 | 35.3 (1.3) | 65.1 (1.3) | 244 (1.7) | 59.6 (1.5) | 84.9 (1.2) |
| Private only, no public coverage | 4.8 | 55.3 | **23.9 (1.3)** | 51.7 (1.3) | 265 (1.7) | **67.1 (1.2)** | 90.0 (0.8) |
| Any coverage | 7.5 | 48.4 | 26.4 (1.2) | 54.6 (1.3) | 261 (1.7) | 65.7 (1.2) | 89.1 (0.8) |
| Uninsured | 23.6 | 21.2 | 37.1 (1.6) | 65.6 (1.4) | 242 (1.9) | 56.8 (2.0) | 82.5 (1.4) |
| All adults 20–65 | 9.3 | 45.3 | 27.6 (1.2) | 55.9 (1.2) | 259 (1.6) | 64.7 (1.3) | 88.3 (0.9) |

Reading the two bold rows: on composition alone, Medicaid enrollees are about **12 points more likely to score at or below Level 1 than privately insured adults (36% vs 24%)**, while their confidence filling out medical forms is only about **7 points lower (60% vs 67% "very confident")**, and five in six in both groups say they are at least somewhat confident. Medicaid enrollees look like uninsured adults on both measures. Weighted population: Medicaid 31.6 million adults 20–65; private only 134.1 million; uninsured 22.9 million.

## Validation

- **Composition check.** PIAAC's own weighted education distribution for 20–65 (8.8 / 44.4 / 46.8%) matches the ACS (9.3 / 45.3 / 45.3%), as expected since PIAAC is raked to ACS controls. HINTS differs (5.3 / 20.3 / 37.3 / 37.1% vs ACS 9.3 / 25.7 / 28.5 / 36.4%): HINTS respondents report less "high school only" and more "some college", which is a known self-report pattern. The bridge removes this by applying ACS composition.
- **Direct check available in HINTS.** HINTS asks insured yes/no, so the bridge can be tested there. Direct HINTS estimate of "very confident", adults 20–65: insured 68.6% (SE 1.3), uninsured 54.3% (SE 3.6). Bridge from composition alone: insured 65.7%, uninsured 56.8%. The bridge reproduces the direction and about 60% of the size of the insured/uninsured gap (8.9 of 14.3 points). The rest is within-cell, which is exactly the part the bridge cannot see. The same should be expected for Medicaid: the true literacy disadvantage is probably larger than 12 points, not smaller.
- **Overall check.** Bridged "all adults 20–65" at or below Level 1 = 27.6%, identical to PIAAC's direct figure (27.6%, NCES publishes 28%).

## Caveats

- Medicaid in ACS is self-reported and includes other means-tested plans; 14% of enrollees aged 20–65 are dual-eligible with Medicare (the second row excludes them; results barely move).
- Ages 20–65 only. HINTS 65+ and Medicaid enrollees 65+ are outside the bridge.
- Cells are coarse (3 age bands) to keep every PIAAC cell above n = 36. A finer-cell sensitivity is cheap to run.
- Standard errors are dominated by the surveys, not the ACS (ACS components are 0.02–0.11 points).

## Files

- `bridge_results.csv`: every estimate with total SE and its ACS and survey components.
- `composition.csv`: ACS cell shares (with SE) for each coverage group, both cell schemes, with the survey's own share for comparison.
- `cells_piaac.csv`, `cells_hints.csv`: cell-level outcome estimates and sample sizes; `.npz` files hold the full replicate arrays.
