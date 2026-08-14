# M3 — CI artifact payload audit — 2026-08-14

## Scope
M3 E8/E12 reproducibility scope. This audit concerns only the public synthetic ERIZO fixture infrastructure; it is **not** a scientific E8/E12 result.

## Workflow
- run_id: `31793329664`
- commit: `7c842feaf63b4d8175537c8906328a046b923998`
- jobs: Python 3.10 (`94744880260`), Python 3.11 (`94744880288`), aggregate
- all jobs: `success`

## Artifacts
Python 3.10:
- artifact_id: `9216353407`
- artifact name: `erizo-fixture-python-3.10`
- archive size: 985 bytes
- archive digest: `sha256:ffacdaff7d8530e8e04c106f88e295f215d74c314686b84f72fd9c21152170bd`

Python 3.11:
- artifact_id: `9216353258`
- artifact name: `erizo-fixture-python-3.11`
- archive size: 985 bytes
- archive digest: `sha256:ffacdaff7d8530e8e04c106f88e295f215d74c314686b84f72fd9c21152170bd`

## Payload audit
Both ZIP archives contain `fixture_results.csv`.

- payload rows: 64
- payload columns: `surface, N, noise_sigma, seed, k, fit_rmse`
- payload byte length: 2661 bytes
- payload SHA-256 (Python 3.10): `343ec6d6410ddd2b27a5845c0b4054435b15ab63dff20f6d90b820e2d4fcb49d`
- payload SHA-256 (Python 3.11): `343ec6d6410ddd2b27a5845c0b4054435b15ab63dff20f6d90b820e2d4fcb49d`
- byte-for-byte payload equality: **YES**

## Verdict
**PASS — CI artifact payload parity.**

This closes the M3 CI/local artifact-payload control. It does **not** establish scientific validity of ERIZO, LASSI, E8 or E12.

## Next action
Create/retain a follow-up task for evidence-index completeness and continue the three E8/E12 diagnostic alternatives: A historical replay, B convergence-safe replay, C provenance-first E12, when the real scientific runtime/artifacts are available.
