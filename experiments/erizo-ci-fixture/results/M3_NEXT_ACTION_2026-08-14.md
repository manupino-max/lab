# M3 next action — 2026-08-14

## Closed this iteration
- Downloaded both CI artifacts.
- Inspected payloads.
- Confirmed 64 rows in each CSV.
- Confirmed identical CSV bytes and SHA-256 across Python 3.10/3.11.
- Stored payload audit and evidence index.

## New follow-up
Artifact/evidence metadata completeness: ensure every promoted run records run_id, job_id, artifact_id, archive digest, payload digest, commit and configuration.

## Still open scientific gates
A. Historical E8 replay.
B. Convergence-safe E8 replay.
C. Provenance-first E12 with Pearson and Spearman.

## Publication candidates
1. Reproducible historical-vs-convergence discrepancy — high potential if it changes scientific interpretation.
2. Reproducible provenance/metric discrepancy — medium-high potential if it changes interpretation.

Neither is currently promoted as a scientific result.
