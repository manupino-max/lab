# Reproducible reproduction suites for candidate papers

These suites re-run the three candidate-paper experiments from scratch in the public lab environment. They intentionally use synthetic/public inputs and emit only aggregate results and run metadata.

## Suites

- `P01_GMRB`: controlled geometric perturbation benchmark; primary check is Dc low-alpha leadership.
- `P02_LEACE_NONLINEAR`: train-only LEACE followed by linear and nonlinear probes, utility and fairness measurements.
- `P03_STRUCTURAL_FRONTIER`: structural distortion vs fairness/utility under controlled representation interventions.

## Reproducibility contract

Each suite fixes its configuration, seed list, and primary metric in code. No private repository checkout is required for the reference implementations. If a private implementation is later used for cross-checking, only aggregate outputs may be exported.

The public lab is a reproduction environment, not the source of truth for unpublished claims. Full scientific records remain in the private research repositories.

## GMR-B governance note

`P01_GMRB` is currently a public reference reproduction/smoke suite. It is **not** treated as an exact implementation-equivalence proof for the investigator GMR-B/DGTLB scientific core. Exact M1 validation remains in the private `-latent-research` repository until the investigator implementation passes the frozen adapter equivalence tests. See `GMRB_AUDIT_2026-08-14.md` for the non-destructive audit.
