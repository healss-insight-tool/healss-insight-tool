#!/usr/bin/env python3
"""ACS 2024 bridge: indirect standardization of PIAAC literacy and HINTS confidence
to the composition of Medicaid enrollees (and other coverage groups).

Reads the ACS 2024 1-year PUMS person file from data/raw/acs2024_pums/ (csv_pus.zip,
or the slim extract acs2024_pus_slim.csv.gz), builds coverage-group composition
across the survey-specific cells from build_cells.py, and computes

    theta_g = sum_c  w_gc * p_c

where w_gc is the ACS share of coverage group g in cell c (80 successive-difference
replicate weights; var = 4/80 * sum (theta_r - theta_0)^2) and p_c is the PIAAC or
HINTS cell estimate (PIAAC: 10 PVs x 44 Fay-BRR replicates, Rubin-combined;
HINTS: 50 jackknife replicates). The two surveys are independent, so
Var(theta) = Var_ACS(sum w_gc^(r) p_c) + Var_survey(sum w_gc p_c^(r)).

Assumption stated plainly: within a cell (education x age band x sex), Medicaid enrollees
are assumed to have the same literacy (or confidence) as all adults in that cell. Anything
that lowers literacy within cells for Medicaid enrollees (disability, language, poverty)
is not captured, so the literacy estimate is best read as a floor on the problem.

Outputs: bridge_results.csv, bridge_results.md, composition.csv in this folder.
"""
import os, sys, zipfile, io, glob, numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.environ.get("ACS_DIR", os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "raw", "acs2024_pums"))
REPS = [f"PWGTP{i}" for i in range(1, 81)]
KEEP = ["AGEP", "SEX", "SCHL", "HICOV", "HINS1", "HINS2", "HINS3", "HINS4", "HINS5", "HINS6", "HINS7",
        "ENG", "DIS", "POVPIP", "PWGTP"] + REPS

def load_acs():
    slim = os.path.join(RAWDIR, "acs2024_pus_slim.csv.gz")
    zips = glob.glob(os.path.join(RAWDIR, "csv_pus*.zip"))
    frames = []
    if os.path.exists(slim):
        print("reading", slim)
        for ch in pd.read_csv(slim, usecols=lambda c: c in KEEP, chunksize=500_000, low_memory=False):
            frames.append(ch[(ch.AGEP >= 20) & (ch.AGEP <= 65)])
    elif zips:
        print("reading", zips[0])
        with zipfile.ZipFile(zips[0]) as z:
            for name in sorted(n for n in z.namelist() if n.lower().endswith(".csv")):
                with z.open(name) as f:
                    for ch in pd.read_csv(f, usecols=lambda c: c in KEEP, chunksize=500_000, low_memory=False):
                        frames.append(ch[(ch.AGEP >= 20) & (ch.AGEP <= 65)])
                print("  ", name, "done")
    else:
        sys.exit("No ACS file found in " + RAWDIR)
    a = pd.concat(frames, ignore_index=True)
    print(f"ACS persons 20-65: {len(a):,}  weighted {a.PWGTP.sum():,.0f}")
    return a

def cells_acs(a, scheme):
    """Return integer cell ids matching build_cells.py ordering (edu, age, sex), -1 if unmatched."""
    s = a.SCHL
    if scheme == "piaac":
        edu = np.select([s <= 15, s.between(16, 19), s >= 20], [1, 2, 3], 0); n_e = 3
    else:
        edu = np.select([s <= 15, s.between(16, 17), s.between(18, 20), s >= 21], [1, 2, 3, 4], 0); n_e = 4
    age = np.select([a.AGEP.between(20, 34), a.AGEP.between(35, 49), a.AGEP.between(50, 65)], [1, 2, 3], 0)
    sex = np.select([a.SEX == 2, a.SEX == 1], [1, 2], 0)   # ACS SEX 1 = male, 2 = female; cells use 1 = F
    ok = (edu > 0) & (age > 0) & (sex > 0)
    cid = (edu - 1) * 6 + (age - 1) * 2 + (sex - 1)
    return np.where(ok, cid, -1), n_e * 6

GROUPS = {
    "Medicaid (HINS4)":            lambda a: a.HINS4 == 1,
    "Medicaid, no Medicare":       lambda a: (a.HINS4 == 1) & (a.HINS3 != 1),
    "Private only (no public)":    lambda a: ((a.HINS1 == 1) | (a.HINS2 == 1)) & (a.HINS3 != 1) & (a.HINS4 != 1) & (a.HINS5 != 1) & (a.HINS6 != 1),
    "Any coverage (insured)":      lambda a: a.HICOV == 1,
    "Uninsured":                   lambda a: a.HICOV == 2,
    "All adults 20-65":            lambda a: np.ones(len(a), bool),
}

def composition(a, cid, n_cells, mask):
    """Shares (n_cells, 81): column 0 = full weight, 1..80 = replicates."""
    W = a[["PWGTP"] + REPS].to_numpy(dtype=float)
    out = np.zeros((n_cells, 81))
    sub = mask & (cid >= 0)
    for c in range(n_cells):
        out[c] = W[sub & (cid == c)].sum(0)
    return out / out.sum(0, keepdims=True)

def combine_piaac(wshare, P):
    """wshare (C, 81) ACS; P (C, 10, 45) PIAAC -> est, se, se_acs, se_piaac."""
    w0 = wshare[:, 0]
    est_pv = np.einsum("c,ck->k", w0, P[:, :, 0])              # per PV with full weights
    est = est_pv.mean()
    # PIAAC variance: per PV, replicates with full ACS weights
    U = np.mean([np.sum((np.einsum("c,cr->r", w0, P[:, k, 1:]) - est_pv[k]) ** 2) / (44 * 0.49) for k in range(10)])
    B = np.var(est_pv, ddof=1)
    v_p = U + 1.1 * B
    # ACS variance: replicate shares with full PIAAC point estimates (mean over PVs)
    p0 = P[:, :, 0].mean(1)
    t_r = np.einsum("cr,c->r", wshare[:, 1:], p0)
    v_a = 4 / 80 * np.sum((t_r - est) ** 2)
    return est, np.sqrt(v_p + v_a), np.sqrt(v_a), np.sqrt(v_p)

def combine_hints(wshare, Q):
    """wshare (C, 81); Q (C, 51) -> est, se, se_acs, se_hints."""
    w0 = wshare[:, 0]
    est = float(w0 @ Q[:, 0])
    t_h = np.einsum("c,cr->r", w0, Q[:, 1:])
    v_h = 0.98 * np.sum((t_h - est) ** 2)
    t_a = np.einsum("cr,c->r", wshare[:, 1:], Q[:, 0])
    v_a = 4 / 80 * np.sum((t_a - est) ** 2)
    return est, np.sqrt(v_h + v_a), np.sqrt(v_a), np.sqrt(v_h)

def main():
    a = load_acs()
    P = np.load(os.path.join(HERE, "cells_piaac.npz")); H = np.load(os.path.join(HERE, "cells_hints.npz"))
    cp = pd.read_csv(os.path.join(HERE, "cells_piaac.csv")); chh = pd.read_csv(os.path.join(HERE, "cells_hints.csv"))
    cid_p, n_p = cells_acs(a, "piaac"); cid_h, n_h = cells_acs(a, "hints")
    rows, comp_rows = [], []
    for g, fn in GROUPS.items():
        m = fn(a).to_numpy() if hasattr(fn(a), "to_numpy") else fn(a)
        n = int(m.sum()); wn = float(a.PWGTP[m].sum())
        wp = composition(a, cid_p, n_p, m); wh = composition(a, cid_h, n_h, m)
        for c in range(n_p):
            comp_rows.append({"group": g, "scheme": "piaac", "cell": c, "education": cp.education[c], "age_band": cp.age_band[c],
                              "sex": cp.sex[c], "acs_share_pct": 100 * wp[c, 0],
                              "acs_share_se": 100 * np.sqrt(4 / 80 * np.sum((wp[c, 1:] - wp[c, 0]) ** 2)),
                              "survey_share_pct": cp.piaac_share_pct[c]})
        for c in range(n_h):
            comp_rows.append({"group": g, "scheme": "hints", "cell": c, "education": chh.education[c], "age_band": chh.age_band[c],
                              "sex": chh.sex[c], "acs_share_pct": 100 * wh[c, 0],
                              "acs_share_se": 100 * np.sqrt(4 / 80 * np.sum((wh[c, 1:] - wh[c, 0]) ** 2)),
                              "survey_share_pct": chh.hints_share_pct[c]})
        for lab, arr in [("Literacy at or below Level 1 (<226), %", P["P_le1"]), ("Literacy below Level 3 (<276), %", P["P_lt3"]),
                         ("Mean literacy score", P["P_mean"])]:
            e, s, sa, sp = combine_piaac(wp, arr)
            rows.append({"group": g, "acs_n": n, "acs_weighted_n": wn, "measure": lab, "source": "PIAAC via ACS", "est": e, "se": s, "se_acs": sa, "se_survey": sp})
        for lab, arr in [("Very confident filling out medical forms, %", H["Q_very"]), ("Very or somewhat confident, %", H["Q_vs"])]:
            e, s, sa, sh = combine_hints(wh, arr)
            rows.append({"group": g, "acs_n": n, "acs_weighted_n": wn, "measure": lab, "source": "HINTS via ACS", "est": e, "se": s, "se_acs": sa, "se_survey": sh})
        # Composition summary for the write-up
        edu_share = {cp.education[c]: 0.0 for c in range(n_p)}
        for c in range(n_p): edu_share[cp.education[c]] += 100 * wp[c, 0]
        rows.append({"group": g, "acs_n": n, "acs_weighted_n": wn, "measure": "Share with no HS diploma, %", "source": "ACS", "est": edu_share["No HS diploma"], "se": np.nan, "se_acs": np.nan, "se_survey": np.nan})
        rows.append({"group": g, "acs_n": n, "acs_weighted_n": wn, "measure": "Share with associate or higher, %", "source": "ACS", "est": edu_share["Associate or higher"], "se": np.nan, "se_acs": np.nan, "se_survey": np.nan})
    res = pd.DataFrame(rows); res.to_csv(os.path.join(HERE, "bridge_results.csv"), index=False, float_format="%.3f")
    pd.DataFrame(comp_rows).to_csv(os.path.join(HERE, "composition.csv"), index=False, float_format="%.3f")
    print(res.to_string(index=False))

if __name__ == "__main__":
    main()
