# M4 → M2 checkpoint 2 — 2026-08-14

## Authority and scope
M4 collaborates only with M2. The approved scope is the M* coordination issue #3. No authority is assumed over M1/M3 or over M2 protocol changes.

## Approved M4 objectives
1. Keep M2 evidence separate from public M4 infrastructure and from M1/M3.
2. Preserve commit → config → run → metrics → artefact → interpretation provenance.
3. Require RAW-vs-POST intervention reporting.
4. Require sensitive leakage + task utility together.
5. Require held-out evaluation and no test tuning.
6. Preserve negative/partial results.
7. Compare claims against concept-erasure literature before promotion.
8. Update the M2 draft only from traceable evidence.
9. Escalate any protocol/scope change to M*.

## New progress since checkpoint 1

### A. Repository lineage verified
Canonical LEACE work in LAB is ordered as:
- `f042d8d6`: canonical LEACE clean-room harness introduced.
- `2efe1d1e`: torch-tensor compatibility fix for canonical LEACE.
- `dbb549a6`: RAW-vs-POST leakage/utility deltas and provenance added.

The latest canonical implementation calls `concept_erasure.LeaceEraser`; it is not the historical hand-written projection.

### B. Evidence schema strengthened
The latest runner records, for each seed:
- RAW linear protected-attribute AUC;
- POST linear protected-attribute AUC;
- linear delta;
- RAW/POST linear balanced accuracy;
- RAW/POST nonlinear (RBF) protected-attribute AUC;
- nonlinear delta;
- RAW/POST task AUC;
- task AUC delta;
- RAW/POST task accuracy;
- seed and runtime package versions in the summary.

This is an evidence-quality improvement because an absolute POST score cannot quantify intervention effect by itself.

### C. Execution status
A non-destructive execution attempt of the canonical runner was made. It is blocked by the current execution environment because `concept_erasure` is unavailable. No manual LEACE substitute was used and no numerical output was promoted.

### D. Governance status
Issue #6 was opened for M* to decide the approved execution environment/source-of-truth for M2. This is a governance escalation, not a protocol modification.

## Pending M2 items — 20
1. M* confirmation of M2 source-of-truth commit/protocol.
2. M* confirmation of canonical execution environment.
3. Freeze primary M2 hypothesis.
4. Freeze falsification criterion.
5. Freeze comparator set.
6. Freeze experimental budget.
7. Freeze seed policy.
8. Freeze RAW baseline definition.
9. Freeze POST definition.
10. Freeze primary leakage metric.
11. Freeze primary utility metric.
12. Freeze probe fitting partition.
13. Freeze final test partition.
14. Verify no test tuning.
15. Pre-specify aggregation/CI.
16. Run canonical LEACE.
17. Save run/config/environment manifest.
18. Save checksums for raw artefacts.
19. Audit leakage/utility and falsification.
20. Promote evidence to M2 draft Results/Methods only after audit and M* acknowledgement.

## Five new issues detected

### N2-1 — Evidence is now effect-oriented
The runner now supports direct RAW→POST deltas rather than only post-intervention values. The draft should use deltas as the intervention-effect quantity, with absolute values retained for context.

### N2-2 — Probe fitting needs explicit partitioning
The current public harness uses train/test separation, but the final M2 protocol should explicitly state whether probe fitting gets its own partition. This is a protocol decision for M*, not a unilateral M4 change.

### N2-3 — Statistical uncertainty is not yet encoded in the canonical output
The runner currently aggregates seed means but does not yet establish the final CI/statistical test. This must be frozen before confirmatory promotion.

### N2-4 — Environment provenance must include dependency identity
Python/Torch/NumPy are recorded, but the final evidence manifest should also capture the exact `concept_erasure` package version/source identity once the approved environment is available.

### N2-5 — Draft language must remain claim-bounded
The M2 narrative should say what the probes demonstrate (e.g. reduced linear detectability under the tested protocol), not claim universal independence. Utility cost must accompany leakage reduction.

## Literature comparison
Belrose et al. (NeurIPS 2023) establish LEACE around linear concept detection. Chowdhury et al. (AISTATS 2025) study fundamental erasure/utility trade-offs. A 2026 CoNLL study uses disjoint space-train, probe-train and test partitions to study estimator/probe generalization. These works support the current M2 design: explicit train/test boundaries, probe-family distinction, and joint leakage/utility reporting.

## Promotion rule
No numerical result from this checkpoint is promoted.

Promotion path:
`M* source-of-truth + environment approval → canonical run → provenance → RAW/POST leakage + utility → uncertainty → falsification → M* acknowledgement → M2 draft update`

## Short-term objectives
- Obtain M* source-of-truth/environment decision.
- Execute canonical LEACE unchanged.
- Produce immutable run/evidence manifest.
- Complete statistical and falsification audit.
- Update M2 Results/Methods from artefacts only.

## Medium-term objectives
- Complete M2 confirmatory evidence chain.
- Compare frozen M2 intervention against frozen comparators under identical budget.
- Execute only pre-specified robustness dimensions.
- Produce a draft-ready evidence table and figures with direct artefact references.
- Preserve and document negative findings.

## Status
`M4/M2 — READY FOR CANONICAL EXECUTION; ENVIRONMENT/GOVERNANCE BLOCKED; NO SCIENTIFIC RESULT PROMOTED`
