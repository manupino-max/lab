# M3 evidence index — 2026-08-14

| Evidence | Commit/run | Status | Scientific claim? |
|---|---|---|---|
| Public ERIZO fixture source | `7c842feaf63b4d8175537c8906328a046b923998` | frozen | No |
| CI run | `31793329664` | PASS | No |
| Python 3.10 job | `94744880260` | PASS | No |
| Python 3.11 job | `94744880288` | PASS | No |
| Artifact 3.10 | `9216353407`, archive SHA-256 `ffacdaff7d8530e8e04c106f88e295f215d74c314686b84f72fd9c21152170bd` | PASS | No |
| Artifact 3.11 | `9216353258`, archive SHA-256 `ffacdaff7d8530e8e04c106f88e295f215d74c314686b84f72fd9c21152170bd` | PASS | No |
| CSV payload parity | SHA-256 `343ec6d6410ddd2b27a5845c0b4054435b15ab63dff20f6d90b820e2d4fcb49d`, 64 rows, byte-identical | PASS | No |
| E8 historical replay | — | EVIDENCE-GATED | Pending |
| E8 convergence-safe replay | — | EVIDENCE-GATED | Pending |
| E12 provenance-first | — | EVIDENCE-GATED | Pending |

## Interpretation rule
The ERIZO fixture PASS establishes public infrastructure reproducibility only. It does not establish E8/E12 scientific validity, LASSI efficacy, fairness improvement, or publication claims.

## Required promotion chain
`commit → configuration → run → job → artifact → payload → metrics → interpretation → draft`

No scientific result is promoted unless all required links are present.
