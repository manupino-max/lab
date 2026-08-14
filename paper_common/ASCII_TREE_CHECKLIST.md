# M2 + M4 experiment tree / checklist

Status key:
- [x] completed and audited
- [~] completed execution, but evidence gate still open
- [>] implementation/specification ready; numerical run/artifact needed
- [!] negative finding retained
- [-] excluded from scientific claims

```text
COMMON PAPER
|
+-- 0. PROTOCOL / AUDIT GATE
|   |
|   +-- [x] Freeze train-only fitting
|   +-- [x] Freeze held-out test evaluation
|   +-- [x] Separate representation metrics from downstream fairness
|   +-- [x] Canonical LEACE = concept_erasure.LeaceEraser
|   +-- [x] Exclude temporary manual "leace()" harness
|   +-- [x] Record workflow/run + artifact + promotion state
|   +-- [x] Keep positive AND negative results
|   `-- [ ] Final consistency audit after all real-data gates
|
+-- 1. M2-P0 CANONICAL LEACE CLEAN-ROOM MATRIX
|   |
|   +-- [x] 20 seeds
|   +-- [x] 5 dimensions
|   +-- [x] 5 intensities
|   +-- [x] 500 configurations
|   +-- [x] Linear protected probe
|   +-- [x] Nonlinear/RBF protected probe
|   +-- [x] Task AUC
|   +-- [x] Held-out evaluation
|   +-- [x] Artifact archived
|   +-- [x] Positive: protected AUC 0.7296 -> 0.5534
|   +-- [x] Positive: nonlinear AUC 0.7218 -> 0.5573
|   +-- [x] Positive: task AUC 0.7573 -> 0.7579
|   +-- [!] Do NOT claim complete nonlinear erasure
|   `-- [~] Promote only after final artifact audit
|
+-- 2. M2-P1 SPARSE / LOCALIZED LEACE PARETO
|   |
|   +-- [x] 20 seeds
|   +-- [x] KFRACS = .02,.05,.10,.20,.40,.60,1
|   +-- [x] lambda = .25,.50,.75,1
|   +-- [x] Raw baseline
|   +-- [x] Full canonical LEACE
|   +-- [x] Sparse candidates
|   +-- [x] Paired Wilcoxon statistics
|   +-- [x] Positive: full LEACE protected AUC = 0.5000
|   +-- [x] Positive: full LEACE task AUC = 0.8607
|   +-- [x] Positive: 60% / lambda=1 protected AUC = 0.7790
|   +-- [!] Negative: sparse is NOT shown superior to full LEACE
|   +-- [!] Negative: synthetic evidence only
|   `-- [~] Final artifact/hash/figure audit
|
+-- 3. M2-P2 MODE / COMMON-SUPPORT H20
|   |
|   +-- [x] Canonical LeaceEraser implementation
|   +-- [x] H = 20 fixed budget
|   +-- [x] 20 seeds specified
|   +-- [x] Train-derived KDE modes
|   +-- [x] Train-derived common-support interval
|   +-- [x] Test selection transferred without test tuning
|   +-- [>] Obtain numerical workflow artifact
|   +-- [>] Audit protected AUC + task AUC across seeds
|   +-- [>] Falsify if unstable / no useful Pareto point
|   `-- [>] Promote only after independent artifact audit
|
+-- 4. M2-R1 MILK10k CANONICAL LEACE
|   |
|   +-- [x] Workflow exists
|   +-- [x] Run 31821347553 completed successfully
|   +-- [>] Retrieve and inspect artifact
|   +-- [>] Verify representation provenance
|   +-- [>] Verify train/validation/test separation
|   +-- [>] Verify canonical LeaceEraser entrypoint
|   +-- [>] Extract protected predictability
|   +-- [>] Extract downstream utility
|   +-- [>] Add fairness outcome metrics where available
|   +-- [>] Compare against unmitigated baseline
|   `-- [>] Promote real-data result
|
+-- 5. M4-T1 MEAN-LINE / GAUSSIAN
|   |
|   +-- [x] Independent synthetic generator
|   +-- [x] Fixed seed 42
|   +-- [x] Full alpha trajectory
|   +-- [x] Protected AUC 0.9447 -> 0.5000
|   +-- [x] Macro-F1 0.7024 -> 0.7500
|   +-- [x] Mean gap 2.3911 -> 0.4476
|   +-- [x] Gaussian KL 3.2142 -> 0.3795
|   +-- [!] Interior optimum hypothesis falsified
|   +-- [!] Equal means != equal distributions
|   `-- [x] Keep as positive + negative evidence
|
+-- 6. M4-T2 UNCONDITIONAL LEACE-CL / MILK10k
|   |
|   +-- [x] Mathematical definition frozen
|   +-- [x] d = mu1 - mu0
|   +-- [x] w = Sw^{-1} d
|   +-- [x] P = d w^T / (w^T d)
|   +-- [x] Pd = d verified
|   +-- [x] Unconditional application rule
|   +-- [x] Synthetic mean equality: ~3.55e-16
|   +-- [>] Run / artifact gate for MILK10k
|   +-- [>] Verify alpha = 0...1 trajectory
|   +-- [>] Compare canonical LEACE
|   +-- [>] Compare utility
|   +-- [>] Compare downstream fairness
|   +-- [>] Falsification: can lose to canonical LEACE and still be valid
|   `-- [>] Promote only after artifact audit
|
+-- 7. M4-A0 PUBLIC HARNESS AUDIT
|   |
|   +-- [x] Temporary helper identified
|   +-- [x] Not canonical LEACE
|   +-- [!] Exclude its numerical outputs from LEACE claims
|   `-- [x] Use only as reproducibility-harness evidence
|
`-- 8. PAPER FINALIZATION
    |
    +-- [x] Springer Nature sn-jnl structure
    +-- [x] M2/M4 section ownership
    +-- [x] ~2-page target per experiment
    +-- [x] Positive results retained
    +-- [x] Negative results retained
    +-- [x] Pending gates explicitly marked
    +-- [ ] Add audited MILK10k numbers
    +-- [ ] Add final figures/tables from artifacts
    +-- [ ] Cross-check every number against artifact
    +-- [ ] Compile LaTeX with Springer template
    +-- [ ] References audit
    +-- [ ] Final claim-strength audit
    `-- [ ] Freeze submission version
```

## Immediate execution order

```text
M2-R1 artifact
     |
     +--> canonical MILK10k result
     |
M4-T2 LEACE-CL artifact
     |
     +--> canonical vs LEACE-CL comparison
     |
M2-P2 H20 artifact
     |
     +--> selective intervention decision
     |
     v
FINAL EVIDENCE TABLE
     |
     +--> every number traced to artifact
     +--> every hypothesis marked SUPPORTED / FALSIFIED / INCONCLUSIVE
     +--> every real-data claim separated from synthetic evidence
     v
SPRINGER COMMON DRAFT v1.0
```

## Promotion rule

```text
RUN SUCCESS
   |
   v
ARTIFACT EXISTS?
   | no --> BLOCK
   | yes
   v
TRAIN/TEST CLEAN?
   | no --> REJECT / rerun
   | yes
   v
CANONICAL IMPLEMENTATION?
   | no --> LABEL EXPLORATORY / exclude claim
   | yes
   v
PRIMARY METRICS + STATS?
   | no --> BLOCK
   | yes
   v
FALSIFICATION CHECK
   |
   +--> supported      -> PROMOTE
   +--> falsified      -> PROMOTE AS NEGATIVE RESULT
   `--> inconclusive   -> RETAIN AS PENDING / do not overclaim
```
