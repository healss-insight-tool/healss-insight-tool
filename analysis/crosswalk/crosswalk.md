# Variable crosswalk: HINTS 7 (2024) × PIAAC Cycle 2 U.S. (2023)

Completed 2026-10-18 against the archived public files and their documentation:
`data/raw/hints7/` (hints7_public.dta, Public Codebook, Annotated English questionnaire, History Document) and
`data/raw/piaac_c2_us/` (PRGUSAP2.sav, OECD Cycle 2 international codebook, Master Background Questionnaire, 2023 Data Analysis Manual).
The machine-readable mapping is in `crosswalk_variables.csv` (one row per construct).

## Gate result

**The Medicaid gate fails, on both sides.**

- HINTS 7 asks one insurance question, C1 `HealthInsurance2`: covered by any health insurance or health care plan, including employer plans or government plans such as Medicare, Medicaid or TRICARE: Yes / No. There is no insurance-type item. "Medicaid" appears in the public codebook only inside that question's wording, and the History Document lists no dropped insurance-type item.
- The OECD PIAAC Cycle 2 U.S. public file has no insurance item at all. `C2_Q11` "received benefits" means unemployment, disability, sickness or retirement benefits in the last 12 months (Master BQ wording).
- The report's first fallback, "any public coverage", is unavailable for the same reasons.
- The NCES U.S. national public file, which the report expected to carry race/ethnicity and U.S.-only health items, was still listed as "forthcoming" on nces.ed.gov on 2026-10-18.

Consequence: H1 (Medicaid enrollees vs privately insured) cannot be tested with public data. The shared subgroup axes that *are* available are education, working-age band, sex and self-rated health. Insured vs uninsured, household income, race/ethnicity and disability exist in HINTS only.

## Shared subgroup definitions (the harmonization codebook)

| Construct | HINTS 7 | PIAAC Cycle 2 | Harmonized definition |
|---|---|---|---|
| Education (primary axis) | `EducA` 1–4 | `EDCAT8_TC1` 1–8 | LT high school = EducA 1 / EDCAT8 1–2 · HS graduate = EducA 2 / EDCAT8 3 · Some college or post-HS training = EducA 3 / EDCAT8 4–5 · Bachelor's or higher = EducA 4 / EDCAT8 6–8 |
| Age band | `Age` (exact, 18–102) | `AGEG5LFS` (16–19 … 60–65) | Primary range **20–65** in both: bands 20–24, 25–34, 35–44, 45–54, 55–65. Sensitivity: PIAAC 16–65 vs HINTS 18–65 |
| Sex | `BirthSex` (1 F, 2 M; drop 3) | `GENDER_R` (1 M, 2 F) | Female / Male. Codes are reversed between surveys |
| Self-rated health | `GeneralHealth` 1–5 | `I2_Q03` 1–5 | Same five labels. Collapse to Excellent/Very good/Good vs Fair/Poor |

Notes on education: PIAAC `EDCAT8_TC1` = 5 is ISCED 5B (associate or professional degree in the U.S. mapping). It sits with "some college" here because HINTS respondents with an associate degree most plausibly chose "Some college" or "Post high school training", not "College graduate". Run a sensitivity with 5B moved to the bachelor's group. Step 0 showed that NCES's own three-way split treats ISCED 4 as "high school" (EDCAT8 3–4) and ISCED 5+ as "more than high school"; the four-level mapping above keeps ISCED 4 with HINTS "some college / post-HS training" because HINTS codes vocational training there (R8 code 4). Both groupings are cheap to run. Sample sizes are comfortable: HINTS LT-HS n = 443, PIAAC EDCAT8 1–2 n = 476.

Notes on age: exact 18–65 is impossible because PIAAC's youngest public band is 16–19. 20–65 lines up exactly (PIAAC `AGEG5LFS` 2–10; HINTS `Age` 20–65, n = 4,256). The OECD file has nobody over 65, so the 66–74 supplement the report mentions is not in it; HINTS 65+ (AgeGrpB 4–5, n = 2,502) gets HINTS-only descriptives, as the report anticipated.

## Outcome measures

**Competence (PIAAC).** `PVLIT1`–`PVLIT10`. Level cut-offs from the 2023 Data Analysis Manual, Table 5.2: below Level 1 < 176; Level 1 176–226; Level 2 226–276; Level 3 276–326; Level 4 326–376; Level 5 > 376. Primary: share at or below Level 1 (score < 226), which is the NCES headline statistic. Sensitivity: share below Level 3 (< 276). A single-PV, full-weight check gives 27.4% below 226 and 56.5% below 276, consistent with the published 28% at or below Level 1 (Step 0 will do this properly with all ten PVs and replicate weights).

**Confidence (HINTS).** `ConfidentMedForms` (C10, "How confident are you filling out medical forms by yourself?") is in HINTS 7 and asked of everyone: Very 4,725 · Somewhat 1,593 · A little 537 · Not at all 259 (valid n = 7,114). Primary: share "Very" confident; sensitivity: "Very" + "Somewhat".

**Difficulty understanding (HINTS).** No HINTS 7 item asks all adults whether health information is hard to understand. The candidates are each filtered to a subpopulation:
- `DigLit_SearchSkills` (B5c, "I have the skills to find the health information I need"): all respondents. Recommended secondary item.
- `ExplainedClearly` (C4e): only those with a provider visit in the past 12 months.
- `UnderstandOnlineMedRec2` (E6): only patient-portal users.
- `CancerTooHardUnderstand` (A2d): only cancer-information seekers.
- `SocMed_TrueFalse` (B14c): only social-media users.

PIAAC adds a behavioural complement: `G2_Q02c`, how often the respondent fills in forms in everyday life (never … every day).

## Weights and variance

| | HINTS 7 | PIAAC Cycle 2 U.S. |
|---|---|---|
| Full-sample weight | `PERSON_FINWT0` | `SPFWT0` |
| Replicates | `PERSON_FINWT1`–`50`, jackknife | `SPFWT1`–`44`, Fay-adjusted BRR, k = 0.3 (`VEMETHOD` = FAY, `VEFAYFAC` = 0.3, `VENREPS` = 44) |
| Variance | (R−1)/R · Σ(θ̂ᵣ − θ̂)², R = 50 | 1/(R(1−k)²) · Σ(θ̂ᵣ − θ̂)² = Σ/21.56, R = 44, then Rubin-combined over 10 PVs |

`SPFWT45`–`SPFWT80` in the U.S. file are copies of `SPFWT0` (padding to the international 80-column layout). They must be excluded; including them with a divisor of 80 would understate PIAAC standard errors. The report's "80 replicate weights" should be corrected to 44.

## Missing-value conventions

- HINTS: negative codes (−9 not ascertained, −7 web partial, −6 filter missing, −5 multiple responses, −4 nonconforming, −2 commission error, −1 inapplicable). Keep −1 separate where the universe matters.
- PIAAC: 6 / 7 / 8 / 9 (or 96–99) = valid skip / don't know / refused / not stated, plus system missing.

## Constructs that do not cross

| Construct | HINTS 7 | PIAAC (OECD public file) | Status |
|---|---|---|---|
| Insurance type / Medicaid | Yes/No only (`HealthInsurance2`) | None | Not available |
| Household income | `HHInc`, 6 ranges, all respondents | Personal earnings deciles, workers only (1,348 missing) | Not comparable; HINTS-only |
| Race/ethnicity | `RaceEthn5` | None | NCES file only |
| Disability | I4 items, `Occupation2_Disabled` | None (people unable to take the assessment are excluded) | HINTS-only |
| Information sources and trust | A3, B3, B12–B14, C11 | None | HINTS-only (RQ4) |
| Language | `Language_Flag` (Spanish completion) | `NATIVELANG`, `HOMLANG` | Exploratory proxy only |
| Digital skills | B5c, B4 | `ICTEVER`, `G2_Q05`, `G2_Q06b` | Exploratory |

## Answers to the report's open questions

1. **Proficiency threshold.** Level 2 as the primary cut (report share < 226, i.e. at or below Level 1); Level 3 (< 276) as the sensitivity.
2. **Primary confidence measure.** `ConfidentMedForms` (C10), confirmed present and universal in HINTS 7. "Very" = high confidence.
3. **Age range.** 20–65 in both surveys. 18–65 cannot be matched exactly; 65+ is HINTS-only.
4. **Phase 2 restricted data.** Required for Medicaid, race/ethnicity and ages 66–74. Two routes: an NCES restricted-use license (the IWU route in the report) once the U.S. file exists, or the OECD Remote Code Execution Service (Stata code run against the restricted files; needs a Master's or PhD and an approved proposal; national variables planned).
5. **Journal.** Not a crosswalk question; unchanged.

## Decision (2026-10-18)

Tyler chose **Education now**: version 1 uses education as the primary subgroup axis (with age band, sex and self-rated health), and the preregistration states that the Medicaid comparison waits for restricted data.

## What this changes in the report

- H1 cannot be tested in version 1. The preregistration needs either a reframed H1 (education and, within HINTS, uninsured adults) or an explicit statement that the Medicaid comparison waits for restricted data.
- "80 replicate weights" → 44 Fay-BRR replicates for PIAAC.
- The data-sources table should name the OECD PUF, not the NCES national file, and drop the 66–74 supplement until the restricted file is in hand.
- Race/ethnicity moves from "Verified" to "NCES file only".

## Addendum (2026-10-19): education coding refined for the ACS bridge

The U.S. PIAAC Cycle 2 public file collapses education to nine ISCED attainment codes (B2_Q01 = 0, 1, 2, 13, 17, 19, 22, 25, 28), which map one-to-one onto `EDCAT8_TC1` 1–8. Because ISCED attainment counts *completed* qualifications, "some college, no degree" is ISCED 3 (EDCAT8 = 3) and ISCED 4 (EDCAT8 = 4, n = 311) is post-secondary certificates. PIAAC therefore cannot separate "high school only" from "some college, no degree". For any comparison against ACS or Census-style education, use NCES's three groups: no HS diploma (EDCAT8 1–2 ↔ ACS SCHL 1–15), HS/GED/some college no degree/certificate (EDCAT8 3–4 ↔ SCHL 16–19), associate or higher (EDCAT8 5–8 ↔ SCHL 20–24). HINTS `EducA` keeps its own four levels (↔ SCHL 1–15 / 16–17 / 18–20 / 21–24). The HINTS–PIAAC four-level mapping in the table above remains usable only with the caveat that PIAAC's "HS graduate" group contains some-college-no-degree adults while HINTS's does not; the ACS bridge (`analysis/acs_bridge/`) avoids this by matching each survey to ACS separately.
