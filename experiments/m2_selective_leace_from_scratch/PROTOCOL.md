# M2 — Selective-LEACE from scratch

## Status

**Protocol initialization only. No scientific run has been executed.**

This experiment is intentionally rebuilt from zero. Existing smoke runners, historical outputs, and exploratory M4/LEACE artifacts are not treated as scientific evidence or as implementation dependencies.

## Scientific scope

Evaluate the frozen M2 intervention protocol for Selective-LEACE, comparing RAW representation against the post-intervention representation under a predeclared evaluation protocol.

M2 remains strictly separated from M1 and M3.

## Required frozen items before execution

- Exact scientific hypothesis.
- Primary falsification criterion.
- Comparator set.
- Experimental budget.
- Seed set (target: 20 seeds, once the protocol is frozen).
- `EPS_F1`.
- `EPS_AUC`.
- `EPS_BA`.
- Dataset/split definition.
- Train-only fitting rule for the intervention.
- Held-out evaluation rule.
- Linear and non-linear attribute probes.
- Utility evaluation.
- Leakage controls.
- Exact software/dependency versions.

## Non-negotiable provenance

Every scientific run must record:

`commit SHA → protocol/config hash → run ID → seeds → environment → metrics → raw artifacts → audit → interpretation`

## Current blockers

1. `EPS_AUC` is not frozen.
2. `EPS_BA` is not frozen.
3. The exact M2 scientific commit/protocol must be declared as the source of truth.
4. The execution workflow must be created and independently auditable.

## Execution gate

The runner MUST refuse scientific execution while any required frozen item is undefined. No threshold may be selected after inspecting test results.

## Planned execution

After the gate is closed:

1. Freeze the protocol and configuration.
2. Build the runner from this clean branch.
3. Run deterministic preflight checks.
4. Execute the complete 20-seed experiment.
5. Store one immutable run manifest per seed and an aggregate manifest.
6. Audit provenance and leakage.
7. Perform a double-check using the frozen configuration.
8. Only then classify the evidence and update the draft.
