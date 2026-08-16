# Related-work comparison — 2026-08-14

## Positioning

The current ERIZO study should not be framed as simply another debiasing method. Existing families primarily optimize or measure removal of protected information and/or preservation of downstream utility. The present study adds a diagnostic layer for residual distributional and geometric structure.

## Comparison

### LEACE
LEACE provides closed-form concept erasure that prevents linear classifiers from detecting a target concept while minimizing representational change under a broad class of norms. The direct comparator is therefore linear concept predictability and representation change.

**Implication for ERIZO:** a lower linear predictability score does not establish that higher-order covariance or geometric structure has disappeared. The benchmark should therefore report both linear leakage and distributional/geometric residuals.

### INLP
INLP repeatedly trains linear classifiers and projects representations onto their null spaces. Its core guarantee/measurement is about linear separability.

**Implication for ERIZO:** residual nonlinear or second-order structure should be treated as a distinct diagnostic target rather than inferred from linear separability.

### Fair representation learning
Recent fair-representation work explicitly optimizes the trade-off between making demographic groups non-separable and preserving task-class separability.

**Implication for ERIZO:** the benchmark must preserve task utility and fairness jointly, but can add geometry/distribution diagnostics to characterize *how* the representation changes.

### Empirical debiasing surveys
Empirical studies report that debiasing methods can behave inconsistently across bias types and that apparent fairness gains can accompany utility degradation.

**Implication for ERIZO:** multi-metric, multi-seed evaluation and Pareto analysis are required before claiming superiority.

## Proposed contribution boundary

The defensible contribution is a **geometry-aware diagnostic and benchmark framework** for residual bias structure, with ERIZO evaluated as one mitigation family inside the benchmark. Superiority is not assumed.

## Evidence status

E8 currently demonstrates optimization-state sensitivity. E12 currently demonstrates a reproducibility/protocol discrepancy. These findings strengthen the need for the diagnostic framing but do not constitute method superiority evidence.
