# M4 — independent mean-line / Gaussian fairness test

## Status
INDEPENDENT TEST / AUTHORIZED

## Purpose
Test, independently of the existing LEACE runner, whether protected-group representations can be moved along the affine line joining their empirical means toward a common target, with the midpoint as the primary target, producing a fairness–utility trade-off or an interior optimum.

## Frozen question
Let `mu0` and `mu1` be training-set protected-group means. For `lambda in {0,.25,.5,.75,1}` define `mu_f(lambda)=lambda*mu0+(1-lambda)*mu1`. For `alpha in {0,.05,...,1}`, transform each group by `z' = z + alpha*(mu_f-mu_g)`.

The primary target is `lambda=.5`, the midpoint. `alpha=1` exactly equalizes the two empirical means. This is **not** equivalent to LEACE: it is a one-dimensional, mean-only intervention.

## Gaussian question
If each group is approximated by a diagonal Gaussian, equalizing means does not by itself make the distributions identical. Therefore the test records symmetric KL divergence between the two fitted diagonal Gaussians. A remaining covariance contribution is evidence against the stronger claim of distributional indistinguishability.

## Primary outcomes
- protected-group predictability: logistic-probe ROC-AUC;
- task macro-F1, balanced accuracy and accuracy;
- Euclidean test-set mean gap;
- diagonal-Gaussian symmetric KL.

## Decision rule
An interior optimum is supported only if some `alpha<1` gives a material fairness improvement while retaining task macro-F1 within the predeclared tolerance of the untransformed baseline, and the pattern is reproduced across independent seeds/splits before promotion.

## Independence requirements
- no LEACE object is fitted or imported;
- target means are computed only from the training split;
- the downstream and protected probes are fitted separately on each transformed training representation;
- test labels/protected attributes are never used to construct the transformation;
- the code is stored under `experiments/`; this document is the testing record.

## Required follow-up
If the midpoint shows an interior optimum, repeat with independent seeds. If it does not, test the competing explanation that fairness gains require covariance-aware or full subspace removal rather than mean transport.
