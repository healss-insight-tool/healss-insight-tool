# HeaLSS Insight Tool

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23537391.svg)](https://doi.org/10.5281/zenodo.23537391) [![OSF](https://img.shields.io/badge/OSF-10.17605%2FOSF.IO%2FCEZTJ-blue)](https://doi.org/10.17605/OSF.IO/CEZTJ)

**Health Literacy Skilling and Scaling.** A data tool that gives insight on existing health-literacy policy and literature by placing two national measurements side by side: how confident U.S. adults say they are with health information (HINTS 7, 2024) and how well they actually read (PIAAC Cycle 2, 2023). It is not a training program.

Study: *Comparing self-reported health-information confidence (HINTS 7, 2024) with measured literacy (PIAAC Cycle 2, 2023) among U.S. adults, by education.*

Authors: Ashley Lewis (first author, project lead; [ORCID 0009-0005-0811-6221](https://orcid.org/0009-0005-0811-6221)) and Tyler L. Jones (second author, data pipeline and statistics; [ORCID 0009-0007-5393-7584](https://orcid.org/0009-0007-5393-7584)), independent researchers.

## Status

| Milestone | State |
|---|---|
| Raw data archived with checksums (HINTS 7, PIAAC Cycle 2 U.S., ACS 2024 PUMS) | done |
| Harmonization codebook (`analysis/crosswalk/`) | done |
| Pipeline validation against published figures (`analysis/step0/`) | done |
| OSF preregistration | registered 2026-10-20: [osf.io/ceztj](https://osf.io/ceztj), DOI [10.17605/OSF.IO/CEZTJ](https://doi.org/10.17605/OSF.IO/CEZTJ) |
| Confirmatory analysis (education gradients, difference in gaps) | done 2026-10-20: [results](analysis/confirmatory/results/results.md). H1 and H2 supported, robust across all sensitivity variants |
| Exploratory Medicaid bridge through the ACS (`analysis/acs_bridge/`) | [results](analysis/acs_bridge/bridge_results.md), disclosed pre-registration pilot |
| Website (`site/`) | live at [healss-insight-tool.github.io](https://healss-insight-tool.github.io/healss-insight-tool/) |
| Release v0.1.0 archived on Zenodo | [10.5281/zenodo.23537391](https://doi.org/10.5281/zenodo.23537391) (2026-10-21) |

## What is here

- `analysis/crosswalk/`: the written codebook that defines identical subgroups (education, age 20 to 65, sex, self-rated health) in both surveys, with the variable-level table.
- `analysis/step0/`: estimation helpers (`survey_est.py`) implementing the HINTS jackknife (50 replicates, factor 0.98) and the PIAAC Fay-BRR variance (44 replicates, k = 0.3) with Rubin combination over ten plausible values, plus the script that reproduces every published HINTS 7 codebook percentage exactly and every NCES 2023 PIAAC figure within rounding.
- `analysis/confirmatory/`: the registered analysis script and its outputs (`results/`): primary estimates, the H1 and H2 tests, five sensitivity analyses, E2 breakdowns and nonresponse tables.
- `analysis/acs_bridge/`: indirect standardization of both measures to the education, age and sex composition of Medicaid enrollees, privately insured and uninsured adults, using the ACS 2024 1-year PUMS with its 80 successive-difference replicate weights.
- `site/`: the single-file project website and its readability checker.
- `data/`: how to obtain the three public-use files and the checksums of the releases used. No microdata are in this repository.

## Reproduce

    pip install -r requirements.txt
    # place the raw files as described in data/README.md
    cd analysis/step0 && python3 step0_reproduce.py
    cd ../acs_bridge && python3 build_cells.py && python3 bridge.py

Python 3.11 or later; tested with pandas 2.x and numpy 1.26 to 2.x.

## Method in one paragraph

Confidence and competence are never measured on the same person. Each quantity is estimated inside its own survey with that survey's weights and replicate variance method; the two are then compared as independent estimates for subgroups defined identically in both. The gap between the confidence share and the literacy share is an index of mismatch between two population-level measures of different constructs, not a within-person discrepancy. Hypotheses, cut-offs and sensitivity analyses were fixed in the preregistration before any gap was computed.

## Headline result (registered analysis, adults 20 to 65)

Measured literacy rises 61 points across education (share at or above PIAAC Level 2, no diploma to bachelor's or higher; 95% CI 54 to 69), but self-reported confidence rises only 30 points (CI 19 to 41). The difference in gaps is 31 points (CI 18 to 45). Among adults with no high school diploma, 46% say they are very confident filling out medical forms while 28% read at Level 2 or above. Both registered hypotheses are supported, and every pre-specified sensitivity variant agrees. Full tables: [analysis/confirmatory/results/results.md](analysis/confirmatory/results/results.md). Plain-language account: [findings_plain_language.md](analysis/confirmatory/results/findings_plain_language.md).

## Citation and licence

Code is released under the MIT licence (`LICENSE`); the codebook and site text under CC BY 4.0. Cite using `CITATION.cff` or the Zenodo record for release v0.1.0: [10.5281/zenodo.23537391](https://doi.org/10.5281/zenodo.23537391). Each tagged release receives its own version DOI on Zenodo.

## Disclosures

Ashley Lewis has worked as a contingent worker for organizations that operate Medicaid managed care plans (UnitedHealthcare, Humana, Centene) and in 2024 as a telephone interviewer for a BRFSS data-collection contractor. None of those organizations had any role in this work, which uses only public-use data. Tyler L. Jones declares no conflicts. Funding: none.
