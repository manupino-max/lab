# M4 → M2 Mantra Checkpoint 3 — 2026-08-14

## Scope and authority
M4 collaborates only with M2. This checkpoint does not decide M1/M3 protocol, execution, or interpretation.

## Standing mantra
1. Work only within approved M4→M2 objectives.
2. Update the draft only from stored, traceable evidence.
3. Compare claims with prior work before promoting novelty claims.
4. Coordinate cross-authority decisions with M*.
5. Maintain at least 10 active M2 pending items.
6. Do not silently change protocol to bypass a stopper.
7. Evaluate 3 distinct stopper-resolution paths.
8. Store any M4-generated evidence in `lab`.
9. Report potentially publishable experiments to M* with novelty/importance and evidence status.
10. Never promote exploratory numbers as confirmatory Results.

## New code-level audit
The canonical harness `experiments/leace_canonical_replication.py` uses `concept_erasure.LeaceEraser`, fits the eraser on the training partition, applies it to train and held-out test, and computes RAW/POST leakage and task-utility metrics. The current file records five seeds (11, 22, 33, 42, 55).

### Confirmed strengths
- Canonical operator is explicit; no manual LEACE substitute.
- RAW and POST are both measured.
- Linear and RBF probes are both represented.
- Utility is measured alongside leakage.
- Test representations are transformed only after fitting the eraser on train.

### Audit items before scientific promotion
- The scientific protocol must freeze whether probe fitting requires a dedicated partition distinct from eraser fitting and final test.
- The primary utility metric and primary leakage metric must be frozen before the confirmatory run.
- Statistical aggregation/CI must be pre-specified.
- Exact `concept_erasure` package/version/commit must be recorded in the final manifest.
- The current synthetic data generator is a harness, not evidence for real-data fairness claims.

## Stopper: three alternatives
### A — approved environment with pinned dependency
Run the canonical file unchanged in an authorized environment containing the exact `concept_erasure` dependency. Preferred for protocol fidelity.

### B — controlled repository CI
Run the same canonical file in authorized GitHub Actions/CI with dependency provenance and artifacts retained. Preferred when CI already defines the approved environment.

### C — infrastructure-only clean-room test
Validate data generation, split logic, metric schema, RAW/POST artifact writing, manifest and checksum machinery without replacing LEACE. This cannot produce scientific LEACE evidence.

No alternative changes the scientific definition silently.

## Literature alignment
LEACE was introduced with a guarantee against linear detection and minimum-change properties within its formulation (Belrose et al., NeurIPS 2023). Recent work identifies an inherent erasure–utility trade-off (Chowdhury et al., AISTATS 2025). CoNLL 2026 reports that LEACE can still show substantial leakage on unseen data, motivating explicit held-out evaluation and caution against interpreting a post-LEACE linear probe as universal independence. These findings support the M2 RAW→POST + linear/nonlinear probe + utility + held-out design.

## Publicability triage
### Potentially high-value, not yet publishable as a result
1. **Canonical LEACE RAW→POST:** high importance; novelty depends on the controlled fairness/utility evaluation and reproducibility.
2. **Linear vs RBF residual leakage:** high importance; potentially strong if nonlinear residual leakage differs materially from linear leakage.
3. **Erasure–utility frontier:** high importance and directly aligned with current concept-erasure theory; potentially the strongest result if reproducible.
4. **Held-out generalization stress test:** high importance because recent work reports unseen-data leakage.
5. **Pre-specified negative/control experiment:** publishable if it falsifies a stated expectation and is reproducibly analyzed.

Current status for all five: `POTENTIALLY_PUBLISHABLE / NOT_RESULT_READY`.

## Active M2 pending list (20)
1. M* source-of-truth commit/protocol
2. Approved execution environment
3. Primary hypothesis wording
4. Primary falsification criterion
5. Comparator set
6. Compute/hyperparameter budget
7. Seed set
8. RAW definition
9. POST definition
10. Primary leakage metric
11. Primary utility metric
12. Probe-fitting partition
13. Final held-out partition
14. No-test-tuning rule
15. Statistical CI/test plan
16. Canonical execution
17. Run/config manifest
18. Artifact checksums
19. Leakage/utility/falsification audit
20. Results promotion decision

## Five newly surfaced control questions
N1. Should probe fitting use a dedicated partition separate from eraser fitting?
N2. What exact package/version/commit of `concept_erasure` is authorized?
N3. Should utility loss be reported as an absolute delta, relative delta, or both?
N4. What minimum evidence package is required before M* acknowledges a result as draft-ready?
N5. Does the confirmatory run require a real/public dataset in addition to the synthetic harness?

## Promotion rule
No numerical result enters M2 Results until:
`source-of-truth + approved environment → canonical run → provenance/checksums → RAW/POST → uncertainty → falsification → M* acknowledgement → draft promotion`.

## Status
`M4→M2: READY FOR AUTHORIZED EXECUTION / NO CONFIRMATORY RESULT PROMOTED`
