"""Confirmatory analysis for the HeaLSS Insight Tool study, as preregistered
on OSF (https://osf.io/ceztj, submitted 2026-10-20).

Quantities (all weighted shares of U.S. adults aged 20 to 65, in percentage points):
  C_g  share "Very" confident filling out medical forms (HINTS 7, ConfidentMedForms = 1)
  P_g  share at or above PIAAC literacy Level 2 (PVLIT >= 226), combined over 10 plausible values
  Gap_g = C_g - P_g;  dC = C_BA+ - C_noHS;  dP = P_BA+ - P_noHS;  D = Gap_noHS - Gap_BA+ = dP - dC
Decision rules: H1 supported if the 95% CI for dP lies above 20 points.
  H2 supported if the CI for D excludes 0 and D > 0; H2-alt if it excludes 0 and D < 0; else inconclusive.
Variance: HINTS jackknife (50 replicates, factor 0.98); PIAAC Fay-BRR (44 replicates, k = 0.3) per
plausible value, Rubin combination V = U_bar + 1.1 B; cross-survey quantities add the two variances.

Safety: the real data are touched only when HEALSS_REGISTERED=1 is set, which happens after the
OSF registration shows "Registered". `--synthetic` runs the whole pipeline on fabricated data.

Usage:
  python3 confirmatory.py --synthetic          # pipeline test, no real data
  HEALSS_REGISTERED=1 python3 confirmatory.py  # the registered run
"""
import argparse, os, sys, json, datetime
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "step0"))
import survey_est as se

Z = 1.959964
EDU3 = {1: "No high school diploma", 2: "High school through associate", 3: "Bachelor's or higher"}
AGE3 = {1: "20-34", 2: "35-49", 3: "50-65"}
SEX = {1: "Female", 2: "Male"}
HEALTH = {1: "Excellent/very good/good", 2: "Fair/poor"}


# ----------------------------------------------------------------------------- estimators
def hints_shares(W, y, mask):
    """W: (n, 51) weights [full, 50 jk]; y: (n,) 0/1; mask: (n,) bool -> (51,) shares in %."""
    Wm, ym = W[mask], y[mask]
    return 100.0 * (Wm * ym[:, None]).sum(0) / Wm.sum(0)


def hints_var(v):
    """v: (51,) estimates -> jackknife variance of v[0]."""
    return se.HINTS_JK_COEF * float(np.sum((v[1:] - v[0]) ** 2))


def piaac_shares(W, Y, mask):
    """W: (n, 45) weights [full, 44 BRR]; Y: (n, 10) 0/1 per plausible value; -> (10, 45) shares in %."""
    Wm, Ym = W[mask], Y[mask]
    num = Ym.T @ Wm            # (10, 45)
    return 100.0 * num / Wm.sum(0)[None, :]


def piaac_combine(A):
    """A: (10, 45) -> (point estimate, variance) by Fay-BRR within PV and Rubin across PVs."""
    R, k = A.shape[1] - 1, se.PIAAC_FAY_K
    t0 = A[:, 0]
    U = np.sum((A[:, 1:] - t0[:, None]) ** 2, axis=1) / (R * (1 - k) ** 2)
    est = float(t0.mean()); Ubar = float(U.mean()); B = float(np.var(t0, ddof=1))
    return est, Ubar + (1 + 1 / len(t0)) * B


def ci(est, var):
    s = float(np.sqrt(var)); return est - Z * s, est + Z * s, s


def logit_ci(p, var):
    """Interval on the logit scale for a share p (in %) with variance var (in points^2); back-transformed."""
    q = p / 100.0; s = np.sqrt(var) / 100.0
    if q <= 0 or q >= 1: return float("nan"), float("nan")
    l = np.log(q / (1 - q)); sl = s / (q * (1 - q))
    lo, hi = l - Z * sl, l + Z * sl
    return 100 / (1 + np.exp(-lo)), 100 / (1 + np.exp(-hi))


# ----------------------------------------------------------------------------- data
def recode_hints(h):
    """Analytic HINTS frame: returns dict of arrays and the nonresponse table."""
    out = {}
    age = h["Age"].to_numpy(float); edu = h["EducA"].to_numpy(float); sex = h["BirthSex"].to_numpy(float)
    cf = h["ConfidentMedForms"].to_numpy(float); b5c = h["DigLit_SearchSkills"].to_numpy(float)
    gh = h["GeneralHealth"].to_numpy(float); form = h["FormType"].to_numpy(float)
    out["age_ok"] = (age >= 20) & (age <= 65)
    out["age25"] = (age >= 25) & (age <= 65)
    out["edu3"] = np.select([edu == 1, (edu == 2) | (edu == 3), edu == 4], [1, 2, 3], 0)
    out["sex"] = np.where(np.isin(sex, [1, 2]), sex, 0).astype(int)
    out["age3"] = np.select([(age >= 20) & (age <= 34), (age >= 35) & (age <= 49), (age >= 50) & (age <= 65)], [1, 2, 3], 0)
    out["health"] = np.select([np.isin(gh, [1, 2, 3]), np.isin(gh, [4, 5])], [1, 2], 0)
    out["cf_valid"] = np.isin(cf, [1, 2, 3, 4])
    out["very"] = (cf == 1).astype(float)
    out["very_somewhat"] = np.isin(cf, [1, 2]).astype(float)
    out["b5c_valid"] = np.isin(b5c, [1, 2, 3, 4])
    out["b5c_strong"] = (b5c == 1).astype(float)
    out["paper"] = form == 2; out["web"] = form == 5
    out["W"] = h[[se.HINTS_W0] + se.HINTS_REPS].to_numpy(float)
    base = out["age_ok"] & (out["edu3"] > 0) & (out["sex"] > 0) & out["cf_valid"]
    out["base"] = base
    # item nonresponse among the age-eligible, unweighted and weighted
    elig = out["age_ok"]
    nr = []
    for name, ok in [("EducA", out["edu3"] > 0), ("BirthSex", out["sex"] > 0), ("ConfidentMedForms", out["cf_valid"]),
                     ("DigLit_SearchSkills (B5c)", out["b5c_valid"]), ("GeneralHealth", out["health"] > 0)]:
        nr.append({"survey": "HINTS 7", "variable": name, "eligible_n": int(elig.sum()),
                   "missing_n": int((elig & ~ok).sum()), "missing_pct_unweighted": round(100 * (elig & ~ok).sum() / elig.sum(), 2)})
    out["nonresponse"] = nr
    return out


def recode_piaac(p):
    out = {}
    ag = p["AGEG5LFS"].to_numpy(float); ed = p["EDCAT8_TC1"].to_numpy(float); sx = p["GENDER_R"].to_numpy(float)
    hl = p["I2_Q03"].to_numpy(float)
    out["age_ok"] = (ag >= 2) & (ag <= 10)
    out["age25"] = (ag >= 3) & (ag <= 10)
    out["edu3"] = np.select([np.isin(ed, [1, 2]), np.isin(ed, [3, 4, 5]), np.isin(ed, [6, 7, 8])], [1, 2, 3], 0)
    out["edu3_5b_up"] = np.select([np.isin(ed, [1, 2]), np.isin(ed, [3, 4]), np.isin(ed, [5, 6, 7, 8])], [1, 2, 3], 0)
    out["sex"] = np.select([sx == 2, sx == 1], [1, 2], 0)
    out["age3"] = np.select([np.isin(ag, [2, 3, 4]), np.isin(ag, [5, 6, 7]), np.isin(ag, [8, 9, 10])], [1, 2, 3], 0)
    out["health"] = np.select([np.isin(hl, [1, 2, 3]), np.isin(hl, [4, 5])], [1, 2], 0)
    PV = p[se.PIAAC_PVS["LIT"]].to_numpy(float)
    out["L2"] = (PV >= 226).astype(float); out["L3"] = (PV >= 276).astype(float)
    out["W"] = p[[se.PIAAC_W0] + se.PIAAC_REPS].to_numpy(float)
    out["base"] = out["age_ok"] & (out["edu3"] > 0) & (out["sex"] > 0)
    elig = out["age_ok"]; nr = []
    for name, ok in [("EDCAT8_TC1", out["edu3"] > 0), ("GENDER_R", out["sex"] > 0), ("I2_Q03", out["health"] > 0)]:
        nr.append({"survey": "PIAAC Cycle 2 U.S.", "variable": name, "eligible_n": int(elig.sum()),
                   "missing_n": int((elig & ~ok).sum()), "missing_pct_unweighted": round(100 * (elig & ~ok).sum() / elig.sum(), 2)})
    out["nonresponse"] = nr
    return out


# ----------------------------------------------------------------------------- one analysis
def run_variant(H, P, name, h_y="very", h_valid="cf_valid", p_ind="L2", h_age="age_ok", p_age="age_ok",
                p_edu="edu3", h_extra=None, groups=("edu3", EDU3), test=True):
    gvar, glab = groups
    hb = H[h_age] & (H["edu3"] > 0) & (H["sex"] > 0) & H[h_valid]
    if h_extra is not None: hb = hb & h_extra
    pb = P[p_age] & (P[p_edu] > 0) & (P["sex"] > 0)
    rows, C, Pm = [], {}, {}
    hg = H[gvar] if gvar != "edu3" else H["edu3"]
    pg = P[gvar] if gvar != "edu3" else P[p_edu]
    for g, lab in glab.items():
        hm = hb & (hg == g); pm = pb & (pg == g)
        c = hints_shares(H["W"], H[h_y], hm); vc = hints_var(c)
        a = piaac_shares(P["W"], P[p_ind], pm); pe, vp = piaac_combine(a)
        C[g] = c; Pm[g] = a
        gap = c[0] - pe; vg = vc + vp
        r = {"variant": name, "group": lab, "n_hints": int(hm.sum()), "n_piaac": int(pm.sum()),
             "C": c[0], "C_se": np.sqrt(vc), "P": pe, "P_se": np.sqrt(vp), "Gap": gap, "Gap_se": np.sqrt(vg)}
        r["Gap_lo"], r["Gap_hi"], _ = ci(gap, vg)
        for lbl, est, var in (("C", c[0], vc), ("P", pe, vp)):
            if est < 10 or est > 90:
                r[f"{lbl}_logit_lo"], r[f"{lbl}_logit_hi"] = logit_ci(est, var)
        rows.append(r)
    tests = None
    if test:
        dc = C[3] - C[1]; vdc = hints_var(dc)
        dpA = Pm[3] - Pm[1]; dp, vdp = piaac_combine(dpA)
        D = dp - dc[0]; vD = vdp + vdc
        dp_lo, dp_hi, _ = ci(dp, vdp); D_lo, D_hi, _ = ci(D, vD); dc_lo, dc_hi, _ = ci(dc[0], vdc)
        h1 = "supported" if dp_lo > 20 else "not supported"
        h2 = "H2 supported" if (D_lo > 0) else ("H2-alt supported" if D_hi < 0 else "inconclusive")
        tests = {"variant": name, "dC": dc[0], "dC_lo": dc_lo, "dC_hi": dc_hi, "dP": dp, "dP_lo": dp_lo, "dP_hi": dp_hi,
                 "D": D, "D_lo": D_lo, "D_hi": D_hi, "H1": h1, "H2_decision": h2}
    return rows, tests


def benchmark_check():
    """Re-run the Step 0 reproduction and halt unless every published benchmark holds."""
    import runpy, contextlib, io
    step0 = os.path.join(os.path.dirname(HERE), "step0")
    cwd = os.getcwd(); os.chdir(step0)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(os.path.join(step0, "step0_reproduce.py"), run_name="__main__")
    finally:
        os.chdir(cwd)
    s = pd.read_csv(os.path.join(step0, "step0_results.csv"))
    worst = s["diff"].abs().max()
    if worst > 0.5:
        raise SystemExit(f"Benchmark check failed: max |diff| = {worst:.2f} > 0.5; halting per registration.")
    return len(s), float(worst)


# ----------------------------------------------------------------------------- synthetic data
def synthetic():
    rng = np.random.default_rng(7)
    n = 4500
    edu = rng.choice([1, 2, 3, 4, -9], n, p=[.07, .17, .3, .44, .02])
    age = rng.integers(18, 95, n).astype(float); age[rng.random(n) < .02] = -9
    sex = rng.choice([1, 2, 3, -9], n, p=[.55, .43, .01, .01])
    lat = 0.2 * np.clip(edu, 1, 4) + rng.normal(0, 1, n)
    cf = np.where(rng.random(n) < .03, -9, np.select([lat > 0.6, lat > 0, lat > -0.6], [1, 2, 3], 4))
    b5c = np.where(rng.random(n) < .02, -9, rng.choice([1, 2, 3, 4], n))
    gh = np.where(rng.random(n) < .03, -7, rng.choice([1, 2, 3, 4, 5], n))
    W = rng.gamma(2, 30000, (n, 51)); W[:, 1:] = W[:, :1] * rng.uniform(0.5, 1.5, (n, 50))
    h = pd.DataFrame({"Age": age, "EducA": edu, "BirthSex": sex, "ConfidentMedForms": cf, "DigLit_SearchSkills": b5c,
                      "GeneralHealth": gh, "FormType": rng.choice([2, 5], n)})
    for i, c in enumerate([se.HINTS_W0] + se.HINTS_REPS): h[c] = W[:, i]
    m = 3700
    ed = rng.choice(list(range(1, 9)) + [np.nan], m, p=[.04, .08, .35, .08, .1, .2, .12, .02, .01])
    ag = rng.choice(list(range(1, 11)), m)
    sx = rng.choice([1, 2], m); hl = rng.choice([1, 2, 3, 4, 5, np.nan], m, p=[.17, .31, .3, .16, .05, .01])
    mu = 200 + 15 * np.nan_to_num(ed, nan=3) + rng.normal(0, 40, m)
    PV = mu[:, None] + rng.normal(0, 15, (m, 10))
    Wp = rng.gamma(2, 30000, (m, 45)); Wp[:, 1:] = Wp[:, :1] * rng.uniform(0.7, 1.3, (m, 44))
    p = pd.DataFrame({"AGEG5LFS": ag, "EDCAT8_TC1": ed, "GENDER_R": sx, "I2_Q03": hl})
    for i, c in enumerate(se.PIAAC_PVS["LIT"]): p[c] = PV[:, i]
    for i, c in enumerate([se.PIAAC_W0] + se.PIAAC_REPS): p[c] = Wp[:, i]
    return h, p


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--synthetic", action="store_true"); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(HERE, "synthetic_test" if a.synthetic else "results")
    os.makedirs(out, exist_ok=True)
    meta = {"run": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "synthetic": a.synthetic,
            "registration": "https://osf.io/ceztj"}
    if a.synthetic:
        h, p = synthetic()
    else:
        if os.environ.get("HEALSS_REGISTERED") != "1":
            raise SystemExit("Refusing to touch the real data: set HEALSS_REGISTERED=1 only once the OSF registration shows 'Registered'.")
        meta["benchmarks_checked"], meta["benchmark_max_abs_diff"] = benchmark_check()
        h, _ = se.load_hints(); p, _ = se.load_piaac()
    H, P = recode_hints(h), recode_piaac(p)

    all_rows, all_tests = [], []
    def add(rows, tests):
        all_rows.extend(rows)
        if tests: all_tests.append(tests)
    add(*run_variant(H, P, "primary"))
    add(*run_variant(H, P, "S1 literacy Level 3", p_ind="L3"))
    add(*run_variant(H, P, "S2a confidence very or somewhat", h_y="very_somewhat"))
    add(*run_variant(H, P, "S2b B5c strongly agree", h_y="b5c_strong", h_valid="b5c_valid"))
    add(*run_variant(H, P, "S3 age 25-65", h_age="age25", p_age="age25"))
    add(*run_variant(H, P, "S4a HINTS paper respondents (full-sample weights)", h_extra=H["paper"]))
    add(*run_variant(H, P, "S4b HINTS web respondents (full-sample weights)", h_extra=H["web"]))
    add(*run_variant(H, P, "S5 PIAAC ISCED 5B moved to bachelor's+", p_edu="edu3_5b_up"))
    # exploratory E2: no tests
    for gv, gl in (("age3", AGE3), ("sex", SEX), ("health", HEALTH)):
        add(*run_variant(H, P, f"E2 by {gv}", groups=(gv, gl), test=False))

    res = pd.DataFrame(all_rows); tst = pd.DataFrame(all_tests)
    nr = pd.DataFrame(H["nonresponse"] + P["nonresponse"])
    # bounds if confidence-item nonresponse exceeds 5% in any education group (registered rule)
    bounds = []
    elig = H["age_ok"] & (H["edu3"] > 0) & (H["sex"] > 0)
    for g, lab in EDU3.items():
        m = elig & (H["edu3"] == g); miss = m & ~H["cf_valid"]
        pct = 100 * miss.sum() / max(m.sum(), 1)
        row = {"group": lab, "cf_missing_pct": round(float(pct), 2)}
        if pct > 5:
            for tag, val in (("all_very", 1.0), ("none_very", 0.0)):
                y = H["very"].copy(); y[miss] = val
                c = hints_shares(H["W"], y, m); row[f"C_bound_{tag}"] = c[0]
        bounds.append(row)
    bounds = pd.DataFrame(bounds)
    res.to_csv(os.path.join(out, "estimates.csv"), index=False)
    tst.to_csv(os.path.join(out, "tests.csv"), index=False)
    nr.to_csv(os.path.join(out, "nonresponse.csv"), index=False)
    bounds.to_csv(os.path.join(out, "confidence_nonresponse_bounds.csv"), index=False)
    with open(os.path.join(out, "run_meta.json"), "w") as f: json.dump(meta, f, indent=2)
    pd.set_option("display.width", 200)
    print("SYNTHETIC TEST, numbers are fabricated" if a.synthetic else "REGISTERED RUN")
    print(tst.round(2).to_string(index=False)); print()
    print(res[res.variant == "primary"].round(2).to_string(index=False)); print()
    print(nr.to_string(index=False)); print(); print(bounds.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
