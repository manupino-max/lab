# M4 → M2 Literature Comparison — 2026-08-14

## Purpose
Keep M2 novelty claims aligned with the current concept-erasure literature.

| Work | What it establishes | Implication for M2 |
|---|---|---|
| Belrose et al., NeurIPS 2023, LEACE | Closed-form concept erasure with a guarantee against linear classifiers under its formulation | M2 must not claim universal independence from linear-probe success/failure alone |
| Chowdhury et al., AISTATS 2025 | Fundamental limits and an erasure–utility trade-off | Utility loss is a first-class outcome, not a secondary metric |
| Naowarat et al., CoNLL 2026 | LEACE can retain substantial leakage on unseen data; concept-subspace estimator choice matters | Held-out/generalization evaluation is essential; nonlinear residual checks are informative |

## M2-specific opportunity
The defensible novelty is not “LEACE exists” or “geometry is used for fairness.” The M2 contribution should be framed, if supported by evidence, as a controlled evaluation of intervention effect using RAW→POST deltas, dual detector families, task utility, held-out generalization, pre-specified falsification, and complete provenance.

## Claim boundary
Avoid:
- “LEACE removes the sensitive attribute completely.”
- “linear probe AUC ≈ 0.5 proves independence.”
- “representation erasure proves causal fairness.”

Prefer:
- “LEACE reduced detectability under the specified detector and evaluation protocol.”
- “Residual nonlinear detectability was/was not observed under the specified robustness probe.”
- “Utility changed by Δ under the held-out task evaluation.”

## Status
Literature comparison is draft-supporting evidence only; no experimental M2 result is promoted by this document.
