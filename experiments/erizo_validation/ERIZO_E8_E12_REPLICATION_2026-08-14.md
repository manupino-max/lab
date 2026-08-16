# ERIZO E8/E12 independent validation snapshot — 2026-08-14

Status: `REPLICATION` / `EXPLORATORY`

This public-lab record documents already-obtained independent checks. It is not a promotion of private historical claims and does not replace the private source-of-truth.

## E8 — convergence sensitivity

Independent implementation, seed 42.

| protocol | convergence | final D_mu | final D_Sigma | interpretation |
|---|---:|---:|---:|---|
| max_iter=50 | no | historical value reproduced | historical value reproduced | non-converged snapshot |
| max_iter=500 | yes, 142 iterations | ~5.4447 | ~46.9315 | materially different converged trajectory |

Conclusion: historical E8 numbers are numerically reproducible but are not stable under convergence control. A publication claim must therefore specify the optimization/convergence state and should not treat the 50-iteration snapshot as convergence evidence.

## E12 — geometric intensity vs mitigation cost

Independent implementation under the documented protocol: seed sequence 42..51, n=1200, d=6, conceptual LEACE-Gauss stages.

- independent Pearson r = **+0.9904**
- independent p ≈ **3.68e-08**
- historical reconciliation = **r=-0.2975, p=0.4039**

Conclusion: the historical E12 result is not reproduced under the documented protocol. This is recorded as an unresolved protocol/provenance discrepancy. The favorable or unfavorable value must not be selected post hoc.

## Scientific use

These records support a stronger research question: mitigation should be evaluated jointly through protected-group predictability, task utility, distributional structure and geometry, rather than a single fairness score. E8 and E12 are diagnostic evidence for protocol sensitivity, not evidence of ERIZO superiority.

## Provenance boundary

The private repository remains the source of truth for unpublished claims. This lab record is intentionally aggregate and public-safe, consistent with the lab governance rule: explore openly; validate rigorously; promote selectively.
