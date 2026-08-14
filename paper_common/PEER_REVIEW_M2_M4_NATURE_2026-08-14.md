# Joint peer review and author-response record — M2/M4

## M4 review of M2 — Nature-style

### Major 1: protected-AUC reduction is over-interpreted
**Critique:** AUC 0.5534 is not indistinguishability; the experiment is synthetic and aggregate uncertainty must be distinguished from fairness.

**Resolution:** The manuscript now calls this protected recoverability, not fairness. Nonlinear residual AUC is retained as evidence against complete empirical erasure. The matrix remains exploratory.

### Major 2: sparse Pareto point may involve test tuning
**Critique:** The 60%/lambda=1 point cannot be called optimal unless selection was independent of test outcomes.

**Resolution:** It is now explicitly a representative/descriptive Pareto point, not an optimum or SOTA result. Confirmatory selection is restricted to train-derived rules; test results are held out.

### Major 3: mean-line contrary result must be foregrounded
**Critique:** Full mean equalization reaches protected AUC 0.5, yet test mean gap and Gaussian KL remain non-zero. The interior-optimum hypothesis also fails.

**Resolution:** Both are explicit falsifications. Mean equality is restricted to a first-moment statement and no generic interior optimum is claimed.

### Major 4: LEACE-CL lacks completed real-data validation
**Critique:** Mathematical validity does not establish empirical validity.

**Resolution:** MILK10k is a separate gate. No real-data numerical claim is promoted until its artifact passes the audit.

### Major 5: relation to canonical LEACE is ambiguous
**Critique:** A reader could mistake LEACE-CL for canonical LEACE.

**Resolution:** Canonical LEACE is the reference baseline; LEACE-CL is a separate rank-one Fisher-separation intervention. No canonical LEACE theorem is attributed to it.

### Major 6: utility AUC alone cannot establish fairness
**Resolution:** Representation recoverability is separated from downstream fairness. Real-data promotion requires demographic parity, equal opportunity and TNR gaps in addition to utility.

### Minor corrections resolved
- pooled covariance is numerically regularized;
- P is a generally non-symmetric rank-one oblique projector/operator, not an orthogonal projector;
- P and mu_f are fitted from training data only;
- AUC=0.5 is called chance-level protected predictability, not perfect fairness;
- every experiment is mapped to workflow/run/artifact/status.

**M4 verdict on M2:** READY under these restrictions.

---

## M2 review of M4 — Nature-style

### Major 1: LEACE-CL proof needs the midpoint algebra
**Critique:** Pd=d alone should not be used to imply arbitrary affine equality; the midpoint identities must be explicit.

**Resolution:** For mu_f=(mu_0+mu_1)/2, mu_0-mu_f=-d/2 and mu_1-mu_f=d/2. Therefore T_1(mu_0)=mu_0+ d/2=mu_f and T_1(mu_1)=mu_1-d/2=mu_f. The guarantee is only for the two fitted group means.

### Major 2: P must not be called orthogonal
**Critique:** P^2=P, but d and w need not be parallel.

**Resolution:** The manuscript uses “rank-one oblique projector/operator”. This distinction is now explicit.

### Major 3: mean-line is not LEACE-CL
**Critique:** The synthetic mean-line intervention conditions on g, while LEACE-CL is unconditional at application time. It cannot be presented as direct deployment validation of LEACE-CL.

**Resolution:** Experiment 3 is now explicitly a first-moment mechanism/falsification test. The unconditional LEACE-CL protocol has its own real-data gate.

### Major 4: the contrary experiments change the central claim
**Critique:** If full alpha wins and the interior optimum fails, the manuscript cannot retain an interior-optimum narrative.

**Resolution:** The interior-optimum hypothesis is marked FALSIFIED and removed as a claimed contribution. The central claim is narrowed to auditable geometric intervention and the distinction between first-moment and distributional equality.

### Major 5: real-data validation incomplete
**Resolution:** MILK10k is labelled pending. No real-data performance is inferred from synthetic experiments; encoder limitations are stated.

### Major 6: negative evidence must be visible
**Resolution:** The manuscript now contains an explicit contrary-evidence section/table and retains falsified hypotheses rather than selecting only favourable trajectories.

**M2 verdict on M4:** READY under these restrictions.

---

## Joint resolution of contrary experiments

| Contrary finding | Scientific threat | Resolution | Status |
|---|---|---|---|
| Full mean equalization, not interior alpha, gives strongest tested protected-AUC reduction | Falsifies generic interior optimum | Remove optimum claim; retain as negative evidence | FALSIFIED / retained |
| Means equalized but Gaussian KL remains 0.3795 | Challenges distributional-equality interpretation | Restrict guarantee to first moment | RESOLVED |
| Nonlinear protected AUC remains ~0.557 after LEACE | Challenges complete-erasure interpretation | Report residual nonlinear recoverability | RESOLVED |
| Sparse point does not beat full LEACE | Challenges superiority/novelty claim | Reframe sparse result as Pareto diagnostic | RESOLVED |
| Evidence is synthetic/clean-room | Challenges external validity | Mark exploratory and require real-data gate | RESOLVED |
| Temporary non-canonical LEACE helper existed | Threatens method identity | Exclude its outputs from LEACE claims | RESOLVED |
| MILK10k LEACE-CL artifact pending | Blocks empirical real-data claim | Do not report numerical result until audit | PENDING GATE |

## Final joint decision

**M2 READY. M4 READY.**

The defensible paper claim is deliberately narrower: canonical LEACE is the linear concept-erasure reference; selective interventions expose a controlled fairness--utility frontier; LEACE-CL is a rank-one Fisher-separation intervention with an exact first-moment property and unconditional application; and the contrary experiments demonstrate that equal means are not distributional indistinguishability and that a generic interior optimum is not supported.

No completed experiment has an unresolved scientific contradiction. The only open item is the separately gated MILK10k LEACE-CL artifact, which is excluded from current quantitative claims.