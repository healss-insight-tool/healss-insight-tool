# Confirmatory results: confidence vs. competence by education

Registered analysis (OSF https://osf.io/ceztj). Run 2026-10-20T23:35:58+00:00 on the archived HINTS 7 and PIAAC Cycle 2 U.S. public-use files, after the Step 0 benchmark check (37 published figures, largest absolute difference 0.5). Adults aged 20 to 65. All figures are weighted percentages with 95% confidence intervals from the surveys' replicate weights. Confidence and competence are measured on different people in different surveys; the gap is an index of mismatch between two population-level measures, not a within-person discrepancy.

## Headline

- **H1 supported.** Measured literacy rises steeply with education: the share at or above PIAAC Level 2 is 61.3 points higher among adults with a bachelor's degree or higher than among adults with no high school diploma (95% CI 53.8 to 68.8), well above the registered 20-point threshold.
- **H2 supported.** Self-reported confidence rises much less with education than measured literacy does: the confidence gradient is 30.0 points (CI 19.0 to 41.0) against the literacy gradient of 61.3. The difference in gaps, D = 31.3 points (CI 18.0 to 44.6), excludes zero and is positive, so the competing H2-alt is not supported.
- Among adults with **no high school diploma**, 45.9% say they are very confident filling out medical forms, but 27.7% score at or above Level 2: confidence exceeds measured literacy by 18.2 points (CI 5.4 to 31.0). In the other two groups the sign reverses: literacy exceeds high confidence by 6.3 points (high school through associate) and 13.1 points (bachelor's or higher).
- Every one of the eight pre-specified sensitivity variants gives the same decisions (H1 supported, H2 supported), so the conclusion is robust under the registered rule.

## Primary estimates (registered education groups)

| Group | HINTS n | PIAAC n | Very confident, % (SE) | Literacy Level 2+, % (SE) | Gap, points (95% CI) |
|---|---|---|---|---|---|
| No high school diploma | 232 | 311 | 45.9 (5.5) | 27.7 (3.5) | 18.2 (5.4 to 31.0) |
| High school through associate | 1746 | 1885 | 63.4 (1.8) | 69.8 (1.7) | -6.3 (-11.2 to -1.5) |
| Bachelor's or higher | 2194 | 1305 | 75.9 (1.6) | 89.0 (1.6) | -13.1 (-17.5 to -8.7) |

Gap = very confident share minus Level 2+ share. Positive means confidence exceeds measured literacy.

## Registered tests

| Quantity | Estimate | 95% CI | Rule | Decision |
|---|---|---|---|---|
| Literacy gradient dP (bachelor's+ minus no diploma) | 61.3 | 53.8 to 68.8 | H1: interval above 20 | supported |
| Confidence gradient dC (bachelor's+ minus no diploma) | 30.0 | 19.0 to 41.0 | component of D | |
| Difference in gaps D = dP minus dC | 31.3 | 18.0 to 44.6 | H2 if CI excludes 0 and D > 0; H2-alt if D < 0 | H2 supported |

## Sensitivity analyses (all pre-specified)

| Variant | dC (CI) | dP (CI) | D (CI) | H1 | H2 decision |
|---|---|---|---|---|---|
| S1 literacy Level 3 | 30.0 (19.0 to 41.0) | 60.0 (53.6 to 66.4) | 30.0 (17.3 to 42.7) | supported | H2 supported |
| S2a confidence very or somewhat | 21.5 (12.7 to 30.2) | 61.3 (53.8 to 68.8) | 39.8 (28.3 to 51.3) | supported | H2 supported |
| S2b B5c strongly agree | 50.8 (44.7 to 57.0) | 61.3 (53.8 to 68.8) | 10.4 (0.7 to 20.1) | supported | H2 supported |
| S3 age 25-65 | 37.1 (27.3 to 46.9) | 64.3 (57.2 to 71.5) | 27.2 (15.1 to 39.3) | supported | H2 supported |
| S4a HINTS paper respondents (full-sample weights) | 38.0 (20.8 to 55.1) | 61.3 (53.8 to 68.8) | 23.3 (4.6 to 42.0) | supported | H2 supported |
| S4b HINTS web respondents (full-sample weights) | 27.8 (12.3 to 43.3) | 61.3 (53.8 to 68.8) | 33.5 (16.3 to 50.7) | supported | H2 supported |
| S5 PIAAC ISCED 5B moved to bachelor's+ | 30.0 (19.0 to 41.0) | 59.3 (51.7 to 66.9) | 29.3 (16.0 to 42.7) | supported | H2 supported |

Notes. S2b uses the secondary confidence item (B5c, "I have the skills to find the health information I need", strongly agree), a different construct from form-filling confidence; its gaps are negative in every group, yet the education gradient in confidence is still smaller than the literacy gradient, so D stays positive (CI 0.7 to 20.1). S4 is a departure from the registration wording: the HINTS 7 public file carries no mode-specific weights, so paper and web respondents are split by form type and estimated with the full-sample weights; both halves give the same decisions.

## Exploratory E2: by age band, sex and self-rated health (intervals only, no tests)

| Breakdown | Group | HINTS n | PIAAC n | Very confident, % | Level 2+, % | Gap (95% CI) |
|---|---|---|---|---|---|---|
| age3 | 20-34 | 995 | 1099 | 56.3 | 76.2 | -19.8 (-26.3 to -13.4) |
| age3 | 35-49 | 1335 | 1114 | 73.3 | 74.0 | -0.7 (-6.4 to 5.0) |
| age3 | 50-65 | 1842 | 1288 | 70.2 | 68.7 | 1.5 (-3.5 to 6.6) |
| sex | Female | 2590 | 1881 | 71.6 | 74.5 | -2.9 (-7.0 to 1.2) |
| sex | Male | 1582 | 1620 | 62.7 | 71.3 | -8.7 (-13.7 to -3.7) |
| health | Excellent/very good/good | 3425 | 2712 | 69.5 | 76.3 | -6.8 (-10.6 to -3.0) |
| health | Fair/poor | 734 | 780 | 54.8 | 60.8 | -6.0 (-13.7 to 1.6) |

The mismatch concentrates in the youngest band (20 to 34), where literacy is highest but reported confidence is lowest, and is absent from age 35 onward. Men report less confidence than women at similar literacy. Fair or poor self-rated health lowers both measures together.

## Item nonresponse (age-eligible respondents, unweighted)

| Survey | Variable | Eligible n | Missing n | Missing % |
|---|---|---|---|---|
| HINTS 7 | EducA | 4256 | 24 | 0.56 |
| HINTS 7 | BirthSex | 4256 | 39 | 0.92 |
| HINTS 7 | ConfidentMedForms | 4256 | 25 | 0.59 |
| HINTS 7 | DigLit_SearchSkills (B5c) | 4256 | 25 | 0.59 |
| HINTS 7 | GeneralHealth | 4256 | 15 | 0.35 |
| PIAAC Cycle 2 U.S. | EDCAT8_TC1 | 3508 | 7 | 0.2 |
| PIAAC Cycle 2 U.S. | GENDER_R | 3508 | 0 | 0.0 |
| PIAAC Cycle 2 U.S. | I2_Q03 | 3508 | 16 | 0.46 |

Nonresponse on the confidence item is below 5% in every education group (No high school diploma: 1.28%, High school through associate: 0.68%, Bachelor's or higher: 0.32%), so the registered bounds rule is not triggered. Complete-case bias from these rates is negligible relative to the estimated gaps.

## Departures from the registration, stated in advance of interpretation

1. Mode sensitivity (S4) uses form type with full-sample weights, because the public file has no mode-specific weights.
2. Analytic samples are slightly smaller than the counts given in the registration (HINTS 4,172 versus 4,231; PIAAC 3,501 versus 3,508), because the registered counts were taken before applying the sex and education validity conditions jointly. No respondent was excluded on any criterion not listed in the registration.
3. The Step 0 benchmark check excludes the two alternative education groupings ("ISCED 3 only", "ISCED 4+") that Step 0 reports as diagnostics to show which grouping NCES uses; the 37 published figures under the NCES grouping all reproduce within 0.5.
4. No confirmatory share fell outside 10% to 90%, so no logit-scale interval was needed.
5. E3 (information channels) is not yet run; it will be reported separately as exploratory.

## Files

`estimates.csv` (every group estimate), `tests.csv` (gradients, D and decisions for every variant), `nonresponse.csv`, `confidence_nonresponse_bounds.csv`, `run_meta.json`. Produced by `../confirmatory.py` with `HEALSS_REGISTERED=1`.
