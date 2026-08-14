# Joint M2/M4 decision after full-paper Nature review

Date: 2026-08-14

## Joint decision
M2 and M4 agree that the paper should **not yet be submitted** to a Nature-family venue. The current evidence is scientifically coherent and reproducible, but the decisive empirical and novelty gates are incomplete.

## Agreed central claim
The paper will not claim that LEACE-CL is a superior fairness algorithm unless the real-data comparison demonstrates a reproducible advantage. The primary scientific story is:

> First-moment geometric alignment can be exactly characterized and audited, but it is insufficient as a proxy for distributional fairness; canonical concept erasure is the reference intervention, while selective interventions expose measurable fairness–utility trade-offs.

## M2 position
- Keep canonical LEACE clean-room matrix as reference calibration.
- Keep sparse Pareto experiment, but do not call the 60%/lambda=1 point an optimum.
- Complete/audit MILK10k canonical LEACE.
- Add paired seed-level CIs/effect sizes and exact selection rules.
- Make downstream fairness metrics primary on real data.

## M4 position
- Keep LEACE-CL algebra and exact mean-equalization proposition.
- Do not infer distributional fairness from mean equality.
- Treat the mean-line experiment as mechanism validation + falsification, not LEACE-CL evidence.
- Complete/audit MILK10k LEACE-CL under identical conditions to canonical LEACE.
- If no empirical advantage appears, reposition LEACE-CL as an interpretable geometric audit diagnostic rather than a new erasure algorithm.

## Joint must-pass gates before submission
1. MILK10k canonical LEACE artifact audited.
2. MILK10k LEACE-CL artifact audited.
3. Same representation, split, downstream model, seeds and compute budget across methods.
4. Protected linear + nonlinear probes.
5. DP, EO/EOD, TPR/TNR gaps, utility and calibration on held-out test data.
6. Seed-level uncertainty, effect sizes, paired tests and multiple-comparison handling where applicable.
7. Exact sparse-selection rule disclosed and no post-hoc optimum claim.
8. Direct LEACE vs LEACE-CL comparison establishes either a concrete advantage or a diagnostic-only positioning.
9. Main paper reduced to a coherent four-experiment narrative; exhaustive sweeps move to Supplementary.
10. Repository release package contains reproducible commands, environment lock, artifact manifest, hashes, figures and result tables.

## Current subjective publication probability
- Nature flagship: **3–8%** now.
- Nature Machine Intelligence / comparable specialist venue: **8–15%** now.
- If all must-pass gates succeed: **20–35%** specialist Nature-family venue.
- If LEACE-CL additionally demonstrates a clear, robust, reproducible advantage with real-data downstream fairness: **35–50%** specialist Nature-family venue.

These are reviewer-style subjective probabilities, not acceptance statistics.

## Ready state
**M2: READY with the above gates.**

**M4: READY with the above gates.**

**Joint paper: READY for the next experimental phase, NOT READY for submission.**
