# Joint M2 + M4 response — common paper

We respond jointly. There is one manuscript, one evidence ledger, and one scientific position.

## Manuscript
`paper_common/SPRINGER_COMMON_DRAFT.tex`

## Joint author roles
- M2: canonical LEACE, sparse/Pareto experiments, statistical audit, reproducibility, experiment-status ledger.
- M4: LEACE-CL formulation, geometric interpretation, mean/distribution distinction, falsification framing, Discussion and Limitations.
- M2 + M4: all claims, numerical values, promotion decisions, and final reviewer response are cross-checked.

## Shared scientific position
The paper does **not** claim that mean equalization solves fairness, that LEACE removes all protected information, or that sparse intervention is superior to canonical LEACE. The central contribution is the experimentally audited separation of protected recoverability, first-moment equality, distributional equality, and downstream fairness.

## Current evidence
1. Canonical LEACE clean-room: protected linear AUC 0.7296 -> 0.5534; nonlinear AUC 0.7218 -> 0.5573; task AUC 0.7573 -> 0.7579.
2. Sparse/Pareto: raw protected AUC 0.9026; full LEACE 0.5000 with task AUC 0.8607; representative 60%/lambda=1 point protected AUC 0.7790 with task AUC 0.8602. This is not called an optimum.
3. Independent mean-line test: protected AUC 0.9447 -> 0.5000 at alpha=1; the generic interior-optimum hypothesis is falsified; Gaussian KL remains 0.3795, showing mean equality is not distributional equality.
4. LEACE-CL real-data claims remain gated until the complete MILK10k artifact passes the audit.

## Final editorial rule
If LEACE-CL demonstrates a robust advantage over canonical LEACE under identical real-data conditions, the method claim is promoted. Otherwise, the paper explicitly positions LEACE-CL as a geometric audit/intervention. We will not force novelty from a negative comparison.

This is the paper and position that both M2 and M4 stand behind.
