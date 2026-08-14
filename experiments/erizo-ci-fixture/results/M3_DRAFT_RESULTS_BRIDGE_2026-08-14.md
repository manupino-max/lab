# M3 draft-results bridge — 2026-08-14

## Results currently admissible
### Public ERIZO fixture reproducibility control
The public synthetic ERIZO fixture was executed by CI on Python 3.10 and Python 3.11 from commit `7c842feaf63b4d8175537c8906328a046b923998`. Both jobs succeeded and verified 64 rows. Their uploaded archives have the same SHA-256 digest, and their extracted `fixture_results.csv` payloads are byte-for-byte identical (64 rows; payload SHA-256 `343ec6d6410ddd2b27a5845c0b4054435b15ab63dff20f6d90b820e2d4fcb49d`).

**Interpretation:** this demonstrates reproducibility of the public synthetic fixture across the two CI Python versions. It does **not** demonstrate scientific validity, fairness efficacy, LASSI efficacy, ERIZO efficacy on real data, or E8/E12 success.

## Results intentionally not yet promoted
- E8 historical replay: no auditable scientific run artifact available.
- E8 convergence-safe replay: no auditable scientific run artifact available.
- E12 provenance-first: required inputs/intermediates and Pearson/Spearman evidence not yet available.

## Drafting rule
Do not place the fixture result in the main scientific Results as evidence for the hypothesis. It belongs, if useful, in a reproducibility/infrastructure subsection or supplementary material.
