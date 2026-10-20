# Project website (version 1)

`index.html` is the single-page site: one HTML file, tab navigation handled in-page, inline SVG charts drawn from the Step 0 numbers, no build step. Published as an Artifact at https://claude.ai/artifact/RwhykYmnGBaJaDTtQp9XAv (private until shared).

To host it elsewhere, upload `index.html` as is; it loads only Google Fonts externally.
`readability.py` scores each tab's prose (Flesch Reading Ease, Flesch–Kincaid grade); rerun it after editing copy and update the table in the Methods tab.
Chart data is embedded in the script block near the bottom (`levels`, `edu`, `forms`, `health`, `verify`); regenerate from `analysis/step0/` when figures change.
