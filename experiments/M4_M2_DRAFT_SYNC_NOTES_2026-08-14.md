# M4 → M2 Draft Synchronization Notes — 2026-08-14

## Rule
The draft is updated only from evidence stored in `lab`. No numerical Results are inserted from exploratory runs, memory, or unverified smoke outputs.

## Methods text that is currently supportable
We evaluate intervention effects using paired RAW-versus-POST measurements. Sensitive-attribute detectability is assessed with linear and nonlinear probes, while downstream task utility is measured on held-out data. The primary intervention effect is defined as the change from RAW to POST. Probe-fitting and final-evaluation partitions must be frozen before confirmatory execution.

## Results status
No numerical M2 result is currently draft-ready because the canonical LEACE execution has not yet completed in an approved environment.

## Evidence references
- Canonical harness: `experiments/leace_canonical_replication.py`
- Evidence Registry: `experiments/M4_M2_EVIDENCE_REGISTRY_2026-08-14.md`
- Stopper options: `experiments/M4_M2_STOPPER_OPTIONS_2026-08-14.md`
- Mantra checkpoint: `experiments/M4_M2_MANTRA_CHECKPOINT_2026-08-14_3.md`

## Claims to avoid
- Do not claim universal independence from a post-LEACE linear probe.
- Do not claim causal fairness from representation leakage alone.
- Do not report the historical P02 smoke output as canonical LEACE evidence.
- Do not describe the synthetic harness as real-data validation.

## Candidate Results table (empty by design)
| Experiment | Primary leakage Δ | Nonlinear residual Δ | Utility Δ | Uncertainty | Falsification | Evidence status |
|---|---:|---:|---:|---|---|---|
| Canonical LEACE | — | — | — | — | — | BLOCKED |
| Linear vs RBF | — | — | — | — | — | BLOCKED |
| Erasure–utility frontier | — | — | — | — | — | BLOCKED |
| Held-out generalization | — | — | — | — | — | BLOCKED |

## Promotion contract
A row can be populated only after canonical execution, complete provenance, pre-specified uncertainty, and falsification audit. The corresponding artifact path/run ID must be recorded in the Evidence Registry.
