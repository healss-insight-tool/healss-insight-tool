# Project website

`index.html` is the whole site: one HTML file, tab navigation handled in-page, inline SVG charts drawn from the Step 0 numbers, no build step and no tracking. It loads only Google Fonts externally, so it can be hosted anywhere a static file can be served, including GitHub Pages for this repository or the project's own domain.

`readability.py` scores each tab's prose (Flesch Reading Ease, Flesch-Kincaid grade); rerun it after editing copy and update the table in the Methods tab.

Chart data is embedded in the script block near the bottom (`levels`, `edu`, `forms`, `health`, `verify`); regenerate from `analysis/step0/` when figures change. No outcome (gap) figures appear on the site until the preregistration is approved.
