"""Weighted estimation with replicate weights for HINTS 7 and PIAAC Cycle 2.

HINTS 7: 50 jackknife replicates, variance = 0.98 * sum_r (theta_r - theta_0)^2
         (NCI HINTS 7 Data Analysis Recommendations: jkcoefs = 0.98, df = 49).
PIAAC:   Fay-adjusted BRR, U.S. file uses 44 replicates with k = 0.3,
         variance = sum_r (theta_r - theta_0)^2 / (R * (1 - k)^2)
         (OECD 2023 Data Analysis Manual, Table 5.1). Plausible values are
         combined with Rubin's rules: V = U_bar + (1 + 1/M) * B.
"""
import os
import numpy as np
import pandas as pd

# Repository root is two levels up; override with HEALSS_RAW=<folder> if the data live elsewhere.
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.environ.get("HEALSS_RAW", os.path.join(_ROOT, "data", "raw"))

HINTS_W0 = "PERSON_FINWT0"
HINTS_REPS = [f"PERSON_FINWT{i}" for i in range(1, 51)]
HINTS_JK_COEF = 0.98

PIAAC_W0 = "SPFWT0"
PIAAC_REPS = [f"SPFWT{i}" for i in range(1, 45)]   # SPFWT45-80 are copies of SPFWT0
PIAAC_FAY_K = 0.3
PIAAC_PVS = {"LIT": [f"PVLIT{i}" for i in range(1, 11)],
             "NUM": [f"PVNUM{i}" for i in range(1, 11)]}

LIT_CUTS = {"below_L1": 176, "L1": 226, "L2": 276, "L3": 326, "L4": 376}


def load_hints():
    import pyreadstat
    df, meta = pyreadstat.read_dta(f"{RAW}/hints7/HINTS7_STATA_20250731/hints7_public.dta")
    return df, meta


def load_piaac():
    import pyreadstat
    df, meta = pyreadstat.read_sav(f"{RAW}/piaac_c2_us/PRGUSAP2.sav")
    return df, meta


def _wstat(y, w, mask, kind):
    """Weighted mean (kind='mean') or proportion of y==True within mask."""
    w = w[mask]
    y = y[mask]
    if kind == "mean":
        return float(np.sum(w * y) / np.sum(w))
    return float(np.sum(w * y) / np.sum(w))  # y is 0/1


def hints_estimate(df, indicator, universe=None):
    """Weighted proportion (in %) of `indicator` (bool Series) among `universe`
    (bool Series; default all rows), with jackknife SE."""
    y = indicator.astype(float).to_numpy()
    mask = np.ones(len(df), bool) if universe is None else universe.to_numpy()
    theta0 = 100 * _wstat(y, df[HINTS_W0].to_numpy(), mask, "prop")
    reps = np.array([100 * _wstat(y, df[r].to_numpy(), mask, "prop") for r in HINTS_REPS])
    var = HINTS_JK_COEF * np.sum((reps - theta0) ** 2)
    n = int(mask.sum())
    total = float(np.sum(df[HINTS_W0].to_numpy()[mask] * y[mask]))
    return {"est": theta0, "se": float(np.sqrt(var)), "n": n, "weighted_n": total}


def piaac_estimate(df, domain, stat, universe=None, lo=None, hi=None):
    """Combine over plausible values.
    stat='mean' -> average score; stat='prop' -> % with lo <= PV < hi.
    universe: bool Series (default all)."""
    mask = np.ones(len(df), bool) if universe is None else universe.to_numpy()
    w0 = df[PIAAC_W0].to_numpy()
    W = np.column_stack([df[r].to_numpy() for r in PIAAC_REPS])
    R, k = len(PIAAC_REPS), PIAAC_FAY_K
    ests, vars_ = [], []
    for pv in PIAAC_PVS[domain]:
        x = df[pv].to_numpy()
        if stat == "mean":
            y = x
            scale = 1.0
        else:
            y = ((x >= (lo if lo is not None else -np.inf)) & (x < (hi if hi is not None else np.inf))).astype(float)
            scale = 100.0
        t0 = scale * _wstat(y, w0, mask, stat)
        tr = np.array([scale * _wstat(y, W[:, j], mask, stat) for j in range(R)])
        ests.append(t0)
        vars_.append(np.sum((tr - t0) ** 2) / (R * (1 - k) ** 2))
    M = len(ests)
    est = float(np.mean(ests))
    U = float(np.mean(vars_))
    B = float(np.var(ests, ddof=1))
    V = U + (1 + 1 / M) * B
    return {"est": est, "se": float(np.sqrt(V)), "n": int(mask.sum())}


def piaac_prop(df, indicator, universe=None):
    """Weighted proportion (in %) of a non-plausible-value indicator (bool Series)
    among `universe`, with Fay-BRR SE (no PV combination)."""
    y = indicator.astype(float).to_numpy()
    mask = np.ones(len(df), bool) if universe is None else universe.to_numpy()
    w0 = df[PIAAC_W0].to_numpy()
    t0 = 100 * _wstat(y, w0, mask, "prop")
    R, k = len(PIAAC_REPS), PIAAC_FAY_K
    tr = np.array([100 * _wstat(y, df[r].to_numpy(), mask, "prop") for r in PIAAC_REPS])
    var = np.sum((tr - t0) ** 2) / (R * (1 - k) ** 2)
    return {"est": float(t0), "se": float(np.sqrt(var)), "n": int(mask.sum())}
