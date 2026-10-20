#!/usr/bin/env python3
"""Cell-level estimates for the ACS bridge (indirect standardization).

Cells, adults 20-65. Each survey uses its own education coding, matched exactly to ACS SCHL:
  PIAAC (18 cells): education 3 levels x age band 3 x sex 2
      E1 no HS diploma (EDCAT8 1-2; ACS SCHL 1-15)
      E2 HS diploma/GED, some college no degree, or certificate (EDCAT8 3-4; ACS SCHL 16-19)
      E3 associate degree or higher (EDCAT8 5-8; ACS SCHL 20-24)
      (ISCED attainment counts completed qualifications, so "some college, no degree" is ISCED 3;
       this is also NCES's own three-way grouping.)
  HINTS (24 cells): education 4 levels x age band 3 x sex 2
      1 LT high school (EducA 1; SCHL 1-15), 2 HS graduate/GED (EducA 2; SCHL 16-17),
      3 post-HS training, some college or associate (EducA 3; SCHL 18-20), 4 bachelor's+ (EducA 4; SCHL 21-24)
  age band: 20-34, 35-49, 50-65 (PIAAC AGEG5LFS 2-4, 5-7, 8-10)
  sex: F, M

PIAAC: for every plausible value (10) and every weight (SPFWT0 + 44 Fay-BRR replicates),
       the weighted share of the cell scoring below 226 (at or below Level 1) and
       below 276 (below Level 3), and the weighted mean literacy score.
HINTS: for every weight (PERSON_FINWT0 + 50 jackknife replicates), the weighted share
       of the cell answering "Very confident" (ConfidentMedForms = 1) and
       "Very or Somewhat" (1-2), among valid answers.

Outputs (this folder): cells.csv (cell definitions + point estimates + SEs),
cells_piaac.npz, cells_hints.npz (full replicate arrays for variance propagation).
"""
import os, sys, numpy as np, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(OUT), "step0"))
import survey_est as se

EDU_P = {1: "No HS diploma", 2: "HS/GED/some college, no degree", 3: "Associate or higher"}
EDU_H = {1: "LT high school", 2: "HS graduate/GED", 3: "Post-HS training/some college/associate", 4: "Bachelor's or higher"}
AGE = {1: "20-34", 2: "35-49", 3: "50-65"}
SEX = {1: "Female", 2: "Male"}
cells_p = [(e, a, s) for e in EDU_P for a in AGE for s in SEX]
cells_h = [(e, a, s) for e in EDU_H for a in AGE for s in SEX]
cell_index_p = {c: i for i, c in enumerate(cells_p)}
cell_index_h = {c: i for i, c in enumerate(cells_h)}

def age_band_from_years(age):
    return np.select([age.between(20, 34), age.between(35, 49), age.between(50, 65)], [1, 2, 3], 0)

# ---------------- PIAAC ----------------
p, _ = se.load_piaac()
ed = p["EDCAT8_TC1"]
p_edu = np.select([ed.isin([1, 2]), ed.isin([3, 4]), ed.isin([5, 6, 7, 8])], [1, 2, 3], 0)
ag = p["AGEG5LFS"]
p_age = np.select([ag.isin([2, 3, 4]), ag.isin([5, 6, 7]), ag.isin([8, 9, 10])], [1, 2, 3], 0)
p_sex = np.select([p["GENDER_R"] == 2, p["GENDER_R"] == 1], [1, 2], 0)
p_ok = (p_edu > 0) & (p_age > 0) & (p_sex > 0)
W = np.column_stack([p[se.PIAAC_W0].to_numpy()] + [p[r].to_numpy() for r in se.PIAAC_REPS])  # (n, 45)
PV = np.column_stack([p[v].to_numpy() for v in se.PIAAC_PVS["LIT"]])                           # (n, 10)
n_c, nw = len(cells_p), W.shape[1]
P_le1 = np.full((n_c, 10, nw), np.nan); P_lt3 = P_le1.copy(); P_mean = P_le1.copy()
p_n = np.zeros(n_c, int); p_wn = np.zeros((n_c, nw))
for c, i in cell_index_p.items():
    m = p_ok & (p_edu == c[0]) & (p_age == c[1]) & (p_sex == c[2])
    p_n[i] = m.sum()
    if p_n[i] == 0: continue
    w = W[m]; pv = PV[m]
    p_wn[i] = w.sum(0)
    for k in range(10):
        x = pv[:, k]
        P_le1[i, k] = 100 * (w * (x < 226)[:, None]).sum(0) / w.sum(0)
        P_lt3[i, k] = 100 * (w * (x < 276)[:, None]).sum(0) / w.sum(0)
        P_mean[i, k] = (w * x[:, None]).sum(0) / w.sum(0)
np.savez(f"{OUT}/cells_piaac.npz", P_le1=P_le1, P_lt3=P_lt3, P_mean=P_mean, n=p_n, wn=p_wn)

def pv_brr_se(A):
    """A: (10 PVs, 45 weights) -> Rubin-combined SE with Fay-BRR (R=44, k=0.3)."""
    t0 = A[:, 0]; tr = A[:, 1:]
    U = np.mean(np.sum((tr - t0[:, None]) ** 2, axis=1) / (44 * 0.49))
    B = np.var(t0, ddof=1)
    return float(np.sqrt(U + 1.1 * B)), float(np.mean(t0))

# ---------------- HINTS ----------------
h, _ = se.load_hints()
h_edu = np.select([h["EducA"] == 1, h["EducA"] == 2, h["EducA"] == 3, h["EducA"] == 4], [1, 2, 3, 4], 0)
h_age = age_band_from_years(h["Age"])
h_sex = np.select([h["BirthSex"] == 1, h["BirthSex"] == 2], [1, 2], 0)
cf = h["ConfidentMedForms"]
h_ok = (h_edu > 0) & (h_age > 0) & (h_sex > 0) & (cf > 0)
HW = np.column_stack([h[se.HINTS_W0].to_numpy()] + [h[r].to_numpy() for r in se.HINTS_REPS])  # (n, 51)
n_h = len(cells_h)
Q_very = np.full((n_h, HW.shape[1]), np.nan); Q_vs = Q_very.copy()
h_n = np.zeros(n_h, int); h_wn = np.zeros((n_h, HW.shape[1]))
for c, i in cell_index_h.items():
    m = (h_ok & (h_edu == c[0]) & (h_age == c[1]) & (h_sex == c[2])).to_numpy()
    h_n[i] = m.sum()
    if h_n[i] == 0: continue
    w = HW[m]; y1 = (cf[m] == 1).to_numpy(); y12 = cf[m].isin([1, 2]).to_numpy()
    h_wn[i] = w.sum(0)
    Q_very[i] = 100 * (w * y1[:, None]).sum(0) / w.sum(0)
    Q_vs[i] = 100 * (w * y12[:, None]).sum(0) / w.sum(0)
np.savez(f"{OUT}/cells_hints.npz", Q_very=Q_very, Q_vs=Q_vs, n=h_n, wn=h_wn)

def jk_se(v):
    return float(np.sqrt(0.98 * np.sum((v[1:] - v[0]) ** 2)))

rows = []
for c, i in cell_index_p.items():
    se1, e1 = pv_brr_se(P_le1[i]); se3, e3 = pv_brr_se(P_lt3[i]); sem, em = pv_brr_se(P_mean[i])
    rows.append({"cell": i, "edu_code": c[0], "education": EDU_P[c[0]], "age_code": c[1], "age_band": AGE[c[1]],
                 "sex_code": c[2], "sex": SEX[c[2]],
                 "n": p_n[i], "piaac_share_pct": 100 * p_wn[i, 0] / p_wn[:, 0].sum(),
                 "lit_le_L1_pct": e1, "lit_le_L1_se": se1, "lit_lt_L3_pct": e3, "lit_lt_L3_se": se3,
                 "lit_mean": em, "lit_mean_se": sem})
dp = pd.DataFrame(rows); dp.to_csv(f"{OUT}/cells_piaac.csv", index=False, float_format="%.3f")
rows = []
for c, i in cell_index_h.items():
    rows.append({"cell": i, "edu_code": c[0], "education": EDU_H[c[0]], "age_code": c[1], "age_band": AGE[c[1]],
                 "sex_code": c[2], "sex": SEX[c[2]],
                 "n": h_n[i], "hints_share_pct": 100 * h_wn[i, 0] / h_wn[:, 0].sum(),
                 "very_confident_pct": Q_very[i, 0], "very_confident_se": jk_se(Q_very[i]),
                 "very_or_somewhat_pct": Q_vs[i, 0], "very_or_somewhat_se": jk_se(Q_vs[i])})
dh = pd.DataFrame(rows); dh.to_csv(f"{OUT}/cells_hints.csv", index=False, float_format="%.3f")
print(dp[["education", "age_band", "sex", "n", "piaac_share_pct", "lit_le_L1_pct", "lit_le_L1_se", "lit_lt_L3_pct", "lit_lt_L3_se"]].to_string(index=False))
print(dh[["education", "age_band", "sex", "n", "hints_share_pct", "very_confident_pct", "very_confident_se"]].to_string(index=False))
print("\nPIAAC 20-65 n =", p_n.sum(), " HINTS 20-65 valid n =", h_n.sum())
print("smallest PIAAC cell n =", p_n.min(), " smallest HINTS cell n =", h_n.min())

# Direct HINTS comparison that needs no bridge: insured vs uninsured, 20-65
ins = h["HealthInsurance2"]
base = h_ok & (ins > 0)
for lab, m in [("insured", base & (ins == 1)), ("uninsured", base & (ins == 2)), ("all 20-65", base)]:
    r = se.hints_estimate(h, cf == 1, m)
    print(f"HINTS very confident, {lab}: {r['est']:.1f}% (SE {r['se']:.2f}, n={r['n']})")
