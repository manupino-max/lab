# M4 — LEACE-CL: linear-combination / maximum-separation test

## Objective
Test the hypothesis that the protected groups can be made linearly indistinguishable by operating on the maximum-separation linear direction between their empirical means, while preserving task utility.

## Definitions
For train representations `Z` and protected groups `g∈{0,1}`:

- `mu0`, `mu1`: train-group means.
- `d = mu1 - mu0`.
- `S = pooled within-group covariance + eps I`.
- Maximum Fisher separation direction: `w = S^{-1} d`.
- Rank-1 LEACE-CL projector: `P = d w^T / (w^T d)`; this is the minimum-rank linear map that removes the group-mean contrast along the Fisher-optimal discriminant while preserving the affine mean target.
- Partial intervention: `Z_a = Z - a P(Z-mu_g)`, `a∈{0,.05,...,1}`.
- At `a=1`, the two transformed train means coincide exactly at their common midpoint.

## Required independent checks
1. Maximum linear protected separation before intervention.
2. Mean equality after `a=1`.
3. Protected linear-probe AUC across the alpha path.
4. Task macro-F1, balanced accuracy and accuracy across the same path.
5. Compare against:
   - raw mean-midpoint transport;
   - canonical LEACE if available;
   - rank-1 LEACE-CL.
6. Diagonal-Gaussian symmetric KL before/after.
7. Train-only fitting: means/covariance/probes are fit on train; test is never used to select alpha.
8. Report the Pareto-feasible best alpha and whether it is strictly interior.

## Falsification
The strong hypothesis is rejected if no interior alpha improves protected fairness while preserving task utility under the pre-registered tolerance. Equality of means alone is not considered proof of indistinguishability.
