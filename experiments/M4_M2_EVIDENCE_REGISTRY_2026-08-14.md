# M4 → M2 Evidence Registry — 2026-08-14

## Scope
M4 collaborates only with M2. This registry does not promote M4 infrastructure or exploratory P02 results as M2 scientific evidence.

## Evidence lineage
- canonical harness: `f042d8d6`
- torch compatibility fix: `2efe1d1e`
- RAW-vs-POST + provenance: `dbb549a6`
- checkpoint: `9c2eb8e77c85fff8b4de59f2fae288ea1e5713fa`

## Current evidence status
| Evidence item | Status | Can enter M2 draft? | Condition |
|---|---|---:|---|
| Canonical LEACE implementation identity | VERIFIED | Yes (Methods/provenance) | Cite exact source/commit |
| RAW/POST schema | VERIFIED | Yes (Methods) | Protocol must adopt it |
| Linear probe design | VERIFIED | Yes (Methods) | Confirm fitting partition |
| RBF probe design | VERIFIED | Yes (Methods) | Confirm as robustness control |
| Utility metrics | VERIFIED | Yes (Methods) | Primary utility metric still to freeze |
| Actual canonical LEACE numerical run | BLOCKED | No | Approved environment with `concept_erasure` |
| Statistical CI/test | PENDING | No | Freeze before confirmatory run |
| Falsification result | PENDING | No | Requires canonical run |

## Draft-ready Methods language (provisional, not yet promoted)
We evaluate intervention effect using paired RAW-versus-POST measurements. Sensitive-attribute leakage is assessed with both a linear probe and a nonlinear RBF probe, while downstream task utility is measured on held-out data. The intervention effect is represented by the change from RAW to POST rather than by the post-intervention value alone. Probe fitting and final evaluation partitions must be fixed before confirmatory execution.

## Draft Results placeholder — intentionally empty
No numerical M2 result is entered here until a canonical LEACE execution is completed in an approved environment and passes provenance, leakage/utility, statistical, and falsification audits.

## Promotion gate
`M* source-of-truth + environment approval`
→ `canonical run`
→ `manifest/checksums`
→ `RAW/POST metrics`
→ `uncertainty`
→ `falsification`
→ `M* acknowledgement`
→ `M2 Results promotion`

## Negative evidence
The current inability to execute because `concept_erasure` is unavailable is recorded as an environment blocker, not as evidence for or against LEACE.
