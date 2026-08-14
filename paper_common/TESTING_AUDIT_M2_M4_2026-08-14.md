# Joint M2/M4 testing audit — 2026-08-14

## Audit rule
A result is promoted only when the experiment has a frozen specification, identifiable workflow/run, deterministic configuration, independent test evaluation, explicit falsification criterion, and a reproducible output artifact. Exploratory results are retained but labelled as such.

## A. M4 independent mean-line / Gaussian test
**Specification:** `testing/M4_MEAN_LINE_GAUSSIAN.md`  
**Results:** `testing/M4_MEAN_LINE_GAUSSIAN_RESULTS.md`  
**CI:** GitHub Actions run `31826211053`, passed after correcting harness/import issues.

Frozen setup: seed 42; 300/300 protected groups; D=12; 240/60 train/test per group; shift in two coordinates; lambda in {0,.25,.5,.75,1}; alpha in {0,.05,...,1}.

Observed trajectory:
- alpha=0: protected AUC 0.9447, task macro-F1 0.7024, test mean gap 2.3911, symmetric diagonal-Gaussian KL 3.2142.
- alpha=.50: protected AUC 0.7914, macro-F1 0.7429, mean gap 1.2554, KL 1.0877.
- alpha=1: protected AUC 0.5000, macro-F1 0.7500, mean gap 0.4476, KL 0.3795.

Audit conclusion: **PASS as independent synthetic validation; exploratory only.** The interior-optimum hypothesis is falsified. Full mean equalization improved the tested fairness proxy but did not make the fitted distributions identical because covariance/shape differences remained.

## B. M4 LEACE-CL specification
**Specification:** `testing/m4_leace_cl_spec.md`.

Target operator:
`d = mu1-mu0`, `w = Sw^{-1}d`, `P = d w^T/(w^T d)`, `T_alpha(z)=z-alpha P(z-mu_f)`, `mu_f=(mu0+mu1)/2`.

The specification correctly requires train-only fitting, protected AUC across alpha, task utility, comparison with canonical LEACE and mean transport, Gaussian KL, and a Pareto/interior-alpha decision rule. Equality of means is explicitly not accepted as proof of indistinguishability.

The associated real-data workflow `31827275170` was still running at audit time. Therefore **no MILK10k numerical result is promoted or written into the manuscript** until its artifact is available and checked.

## C. M2 canonical LEACE clean-room matrix
**Workflow:** `m4-leace-canonical-replication.yml`, successful run `31825302983`.  
**Artifact:** `m4-leace-canonical-replication-0b8110fda0b13d2c44c4ea16f3717e6bd58b1fc6`.

500 configurations: 20 seeds x 5 dimensions x 5 intensities.

Artifact summary:
- linear protected AUC*: 0.7296384 -> 0.5533500 (delta -0.1762884);
- nonlinear protected AUC*: 0.7218170 -> 0.5573060 (delta -0.1645110);
- protected balanced accuracy after: 0.5292600;
- task utility AUC: 0.7573084 -> 0.7579225 (delta +0.0006141).

The artifact itself labels status `exploratory_pending_audit`. Joint audit therefore keeps these values as **exploratory clean-room evidence**, not as final real-data evidence.

## D. M2 sparse/localized LEACE Pareto
**Workflow:** `m2-leace-sparse-pareto.yml`, run `31826906699`, success.  
**Artifact:** `M2_LEACE_SPARSE_PARETO_20260814`, SHA-256 `7e78d886aabb9f19731624f7347d5e1c588c49537015b12bf7ed4816bf8a9f3a`.

20 seeds, N=1200, D=32, KFRACS={.02,.05,.10,.20,.40,.60,1}, lambdas={.25,.50,.75,1}.

Baseline raw: protected AUC 0.9025586 +/- 0.0145988; task AUC 0.8596726 +/- 0.0182285.

Full canonical LEACE: protected AUC 0.5000000 +/- 0; task AUC 0.8607138 +/- 0.0165824; delta task AUC +0.0010412; Wilcoxon p=0.08969.

Selected sparse Pareto point: kfrac=.60, lambda=1: protected AUC 0.7790340 +/- 0.0168693; task AUC 0.8601984 +/- 0.0167822; delta protected AUC -0.1235247; delta task AUC +0.0005257; Wilcoxon p for protected AUC delta <1e-4.

Audit conclusion: **PASS as reproducible synthetic Pareto evidence; exploratory.** The result supports a fairness/utility Pareto interpretation but does not establish superiority over canonical LEACE.

## E. Historical harness exclusion
`experiments/M4_AUDIT_V13.md` correctly identifies `experiments/reproducible_three_papers.py` as a temporary syntax-safe replacement, not canonical LEACE. Its outputs are excluded from scientific LEACE claims.

## Joint scientific position
1. Canonical LEACE is the reference intervention for linear concept erasure.
2. Mean-line transport and LEACE-CL are distinct interventions and must not be conflated.
3. Equalizing empirical group means is a first-moment result, not distributional indistinguishability.
4. The current synthetic evidence supports measurable reduction in protected linear/nonlinear predictability with little task-utility change, but does not justify universal fairness claims.
5. Real MILK10k results remain a separate gate and must be audited before promotion.
