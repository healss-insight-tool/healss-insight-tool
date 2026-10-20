# analysis/acs_bridge

Indirect standardization of PIAAC literacy and HINTS confidence to the composition of Medicaid enrollees, using the ACS 2024 1-year PUMS. See `bridge_results.md` for method, results, validation and caveats.

Run order (needs the archived raw files under `data/raw/`):

    python3 build_cells.py   # cell-level survey estimates with replicate arrays
    python3 bridge.py        # ACS composition, combination, bridge_results.csv/.md inputs

`bridge.py` honours `ACS_DIR=<folder>` for testing against a different ACS extract.
