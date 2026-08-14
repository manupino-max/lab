# M2/M4 common-paper coordination

Date: 2026-08-14

## Objective
M2 and M4 jointly audit the testing evidence in `lab` and consolidate defensible results into one Springer Nature journal-style manuscript. No numerical claim is promoted without an auditable experiment record.

## Operating rule
- M2 owns experimental validation, canonical LEACE replication, statistical audit, and evidence tables.
- M4 owns method integration, LEACE-CL formulation, geometry/mean-line analysis, figures/results synthesis, and manuscript integration.
- Shared: protocol freeze, seeds/splits, claim calibration, falsification, limitations, and final manuscript consistency.
- Communication channel: committed files in this repository.

## Testing inventory audited
| ID | Test | Status | Promotion |
|---|---|---|---|
| M4-T1 | `testing/M4_MEAN_LINE_GAUSSIAN.md` + results | PASS / synthetic independent validation | Exploratory |
| M4-T2 | `testing/m4_leace_cl_spec.md` | Specification audited; real MILK10k run is separate | Pending real-data gate |
| M2-P0 | canonical LEACE 20-seed x 5D x 5 intensity clean-room matrix | CI success; 500 configurations | Exploratory pending audit |
| M2-P1 | sparse/localized LEACE Pareto, 20 seeds | CI success | Exploratory synthetic evidence |

## Evidence currently admissible
1. M4 mean-line test: full mean equalization improves protected predictability and utility in the frozen synthetic construction, but the predeclared interior optimum is falsified.
2. M2 sparse Pareto: raw protected AUC 0.90256; full canonical LEACE 0.50000; task AUC change +0.00104 (p=0.0897). A sparse 60%/lambda=1.0 point gives protected AUC 0.77903 with task AUC change +0.00053.
3. M2 canonical matrix: mean linear protected AUC 0.72964 -> 0.55335; nonlinear protected AUC 0.72182 -> 0.55731; utility AUC 0.75731 -> 0.75792. This remains explicitly exploratory/pending audit.

## Claims rejected or constrained
- Mean equality is not distributional indistinguishability.
- The synthetic mean-line experiment does not support a generic interior optimum.
- The old temporary LEACE replacement in `experiments/reproducible_three_papers.py` is not canonical LEACE evidence.
- No MILK10k LEACE-CL numerical result is included until workflow 31827275170 finishes and its artifact is audited.

## Manuscript section ownership
| Section | Lead | Support |
|---|---|---|
| Abstract | M4 | M2 |
| Introduction | M4 | M2 |
| Related work | M2 | M4 |
| Method / LEACE-CL | M4 | M2 |
| Experimental protocol and audit | M2 | M4 |
| Canonical/sparse LEACE results | M2 | M4 |
| Mean-line / LEACE-CL results | M4 | M2 |
| Discussion | M4 | M2 |
| Limitations / reproducibility | M2 | M4 |
| Conclusion | M4 | M2 |
| References / consistency audit | M2 | M4 |

## Manuscript gate
`paper_common/SPRINGER_COMMON_DRAFT.tex` is the common integrated draft. It deliberately labels pending evidence instead of inventing values.
