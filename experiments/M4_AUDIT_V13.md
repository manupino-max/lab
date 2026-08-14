# M4 LAB Audit v13 — safe protocol audit

Date: 2026-08-14

## Scope
Static audit of the public LAB reproducibility harness before any new numerical result is promoted to the private testing repository.

## Findings

1. `experiments/reproducible_three_papers.py` is explicitly a temporary syntax-safe replacement and therefore is **not** a canonical LEACE implementation.
2. Its `leace()` function estimates a single protected-direction vector by least squares and applies a manual projection. It does not call the canonical `concept_erasure` LEACE implementation used by the existing M2 evidence.
3. Therefore P02 in this public harness must be classified `EXPLORATORY/REPLICATION-HARNESS`, not `PROMOTE` as LEACE evidence.
4. The script does provide useful clean-room infrastructure: runtime synthetic generation, fixed seeds `[11,22,33,44,55]`, CSV output and JSON summary.
5. The public LAB README explicitly states that exploratory results are not automatically research evidence.
6. `experiments/public_runner.py` is independent of private data and demonstrates the desired clean-room pattern: generated inputs, deterministic seed, committed output schema.

## Scientific consequence
Do not use any P02 numerical output as a LEACE claim until the runner is replaced with the canonical LEACE operator and the protocol is aligned with M4 C0.

## Safe next LAB action
Build a separate `LEACE_CANONICAL_REPLICATION` runner using `concept_erasure` and a synthetic dataset generated at runtime. It should output orientation-invariant AUC, balanced accuracy, nonlinear probe AUC, and task utility. It must not overwrite existing P02 outputs.

## Status
`AUDITED — NO NEW SCIENTIFIC RESULT PROMOTED`
