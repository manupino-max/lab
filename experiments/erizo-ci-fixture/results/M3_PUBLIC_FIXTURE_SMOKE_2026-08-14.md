# M3 public ERIZO fixture smoke — 2026-08-14

## Scope
This is a **public synthetic fixture / infrastructure smoke**, not a scientific M3 E8/E12 result. It is deliberately kept separate from thesis-sensitive evidence.

## Source
- Commit: `12b54995e68cec971621bca1b363af9eb96bbd7b`
- Fixture: `experiments/erizo-ci-fixture/run_fixture.py`
- Workflow: `.github/workflows/erizo-fixture.yml`

## Independent local replay
The exact fixture logic was replayed locally from the frozen source above, without changing the scientific code.

Expected matrix:
- surfaces: 4
- N: 2
- noise: 2
- seeds: 2
- k: 2
- expected rows: 64

Observed:
- rows generated: **64**
- finite RMSE values: **64/64**
- RMSE min: **0.0**
- RMSE max: **0.29860021818700566**

## Interpretation
This closes only an **infrastructure/synthetic-fixture smoke check**: the public fixture logic is executable and produces the expected 64-row matrix with finite outputs.

It does **not** validate ERIZO scientific claims, E8, E12, ISIC, LASSI, or any thesis result.

## Evidence policy
The public fixture README states that it uses synthetic data generated at runtime and a deliberately reduced grid. The CI workflow independently checks that the result file exists and contains 64 rows. This evidence is therefore suitable as public reproducibility infrastructure evidence, not as scientific efficacy evidence.

## M3 status
- E8/E12: **still evidence-gated**.
- Public fixture smoke: **PASS (infrastructure only)**.
- No M1/M2/M4 scope assumed.
- Next M3 action: continue independent controls and, when the real E8/E12 runtime/artifacts become available, execute A historical replay → B convergence-safe replay → C provenance-first E12.
