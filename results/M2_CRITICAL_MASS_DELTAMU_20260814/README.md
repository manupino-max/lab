# M2 — Critical mass along Δμ

## Result
On the frozen controlled mean-shift construction, the first 5%-grid level that drives held-out oriented linear protected-group AUC to <= 0.52 is **0.95** both when:

1. the whole protected group is shifted continuously by `dose * (mu1-mu0)`, and
2. only a fraction `mass` of protected-group samples are shifted by the full `-(mu1-mu0)`.

At 0.90 the mean linear AUC remains 0.53376 (dose) and 0.52948 (mass); at 0.95 it is 0.51756 and 0.51692; at 1.00 it is 0.51448. Hence the practical finite-sample detection threshold is reached at approximately **95% of the Δμ separation/mass** on the tested grid.

## Scientific interpretation
The population mean component is mathematically canceled at 100%, but the empirical held-out AUC does not become exactly 0.5 because of finite-sample estimation and noise. Therefore the correct M2 conclusion is a **practical critical mass ≈95%**, not a claim that 95% is an exact population threshold.

This experiment isolates the mean-shift channel. It does not establish complete concept erasure under covariance or nonlinear mechanisms.

## Reproducibility
- 20 seeds
- D=32
- n0=n1=1200
- 70/30 held-out split per seed
- dose grid: 0..1.25 step 0.05
- mass grid: 0..1 step 0.05
- covariance controls: 1.0 and 1.5
- raw matrix: 1880 rows
- raw matrix SHA-256: `246994d27be2e06f2472d68bdf473c4dbf139bbe89c96594bd59d149f67c7c0d`
- source commit: `68e4ca44fc800a50170606c0b63b6f4c56920ed3`
- Actions runs: `31825186014`, `31825221209`

The exact source and workflow are under `experiments/m2_critical_mass_deltamu_numpy.py` and `.github/workflows/m2-critical-mass-fast.yml`.
