# Data: how to obtain the input files

No survey microdata are in this repository. The three public-use files below are downloaded from their official sites and placed under `data/raw/` exactly as listed. The `SHA256SUMS.*` files in this folder let you confirm you have the same releases the results were computed from (`sha256sum -c SHA256SUMS.hints7` from inside the matching folder).

| Survey | Release used | Where | Put it in |
|---|---|---|---|
| HINTS 7 (2024), National Cancer Institute | Stata public-use release `HINTS7_STATA_20250731` | https://hints.cancer.gov/data/download-data.aspx | `data/raw/hints7/` (unzip in place) |
| PIAAC Cycle 2 (2023) U.S. public-use file, OECD | `prgusap2` (SPSS `.sav` and CSV) | https://www.oecd.org/en/about/programmes/piaac/piaac-data.html | `data/raw/piaac_c2_us/` |
| ACS 2024 1-year PUMS, U.S. Census Bureau | `csv_pus.zip` (released 2025-12-04), plus `PUMS_Data_Dictionary_2024.csv` and `2024AccuracyPUMS.pdf` | https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/ | `data/raw/acs2024_pums/` |

Each survey's terms of use forbid redistribution of the microdata, which is why only checksums are kept here.

## ACS slim extract

The full PUMS zip is roughly 650 MB. `slim_pums.py` reads it and writes `acs2024_pus_slim.csv.gz` (ages 18 to 66, the analysis variables, the person weight and its 80 replicate weights, about 240 MB), which is what `analysis/acs_bridge/bridge.py` reads by default:

    python3 slim_pums.py csv_pus.zip

It prints the SHA-256 of the original zip so the archive copy can be verified later.
