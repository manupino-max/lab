# P01_GMRB public-lab audit — 2026-08-14

## Purpose

This file records a non-destructive audit of the public reproduction suite against the private M1 GMR-B validation protocol. It does **not** alter the P01 implementation or promote its output to scientific evidence.

## Finding

The current `P01_GMRB` implementation is a **reference reproduction/approximation**, not an executable copy of the investigator's GMR-B/DGTLB scientific core.

The public script currently defines its own simple synthetic quantities for `Dc`, `Dg`, and `Ds`, and applies 11 named perturbation families over a small synthetic configuration. This is useful as a public smoke/reproduction environment, but it cannot establish equivalence with the investigator notebook.

The public-lab README already states the correct governance boundary: the lab is a reproduction environment, while the private research repositories remain the source of truth for unpublished claims. This audit makes that boundary explicit for GMR-B.

## Consequence for M1

Do **not** use P01 results as evidence for the M1 COMPAS validation or as proof of the investigator result. M1 must instead:

1. freeze the investigator implementation commit;
2. extract the scientific core from `paper_nature_v2.ipynb` / associated reproduction harness;
3. pass adapter equivalence tests E1–E7;
4. run the frozen M1 real-data protocol;
5. export only aggregate/public-safe outputs to `lab` if a public reproduction is later required.

## Safe use of P01

P01 can still be used for:

- CI/smoke testing;
- public demonstration of the experiment concept;
- checking result-file schemas;
- testing plotting and aggregation code;
- demonstrating the distinction between public reproduction and private scientific validation.

## Important negative result

The public P01 implementation should **not** be described in the paper as a reproduction of the investigator's exact GMR-B definitions unless an equivalence test is added and passed.

This audit is intentionally documentation-only; no scientific definition, seed, alpha grid, or result was changed.
