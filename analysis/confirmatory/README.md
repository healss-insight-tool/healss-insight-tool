# analysis/confirmatory

The registered analysis (OSF https://osf.io/ceztj). `confirmatory.py` computes the confidence share, the literacy share, the gap, the two education gradients and the difference in gaps for the three preregistered education groups, applies the registered decision rules for H1 and H2 versus H2-alt, runs the five pre-specified sensitivity analyses and the E2 exploratory breakdowns, tabulates item nonresponse, and applies the nonresponse bounds rule.

Two guards from the registration are built in: the run first repeats the Step 0 benchmark reproduction and halts if any published figure fails to reproduce within 0.5 points, and the real data are only read when `HEALSS_REGISTERED=1` is set, which happens once the registration shows "Registered".

    python3 confirmatory.py --synthetic            # pipeline test on fabricated data (writes synthetic_test/)
    HEALSS_REGISTERED=1 python3 confirmatory.py    # the registered run (writes results/)

Deviation noted in advance: the HINTS 7 public file carries no mode-specific weights, so sensitivity analysis 4 (paper versus web) splits respondents by `FormType` and uses the full-sample weights, which is a descriptive comparison rather than two separately weighted estimates.
