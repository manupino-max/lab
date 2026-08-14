# M4→M2 stopper-resolution log — 2026-08-14

## Scope / authority
M4 only supports M2. This document does not alter M2 protocol, comparators, seeds, budgets, or claims. It records three non-destructive alternatives for resolving the current canonical-LEACE execution stopper.

## Approved objective alignment
Short-term: turn the canonical LEACE runner into reproducible, auditable M2 evidence.
Medium-term: produce draft-ready evidence only after canonical execution, statistics, and falsification.

## Current stopper
The canonical runner requires `concept_erasure`. The current execution environment reported `ModuleNotFoundError: concept_erasure`.

## Alternative A — approved environment / dependency installation
Goal: execute the existing canonical runner unchanged in an environment where the pinned `concept_erasure` dependency is available.

Advantages: highest protocol fidelity; no implementation substitution.
Risks: dependency/version drift unless exact package/version/commit is recorded.
Promotion: eligible if provenance and held-out controls pass.

## Alternative B — repository/CI execution
Goal: run the exact canonical runner through the repository's controlled CI/Actions environment, using the committed dependency specification if present.

Advantages: reproducible environment and durable run provenance.
Risks: requires confirmation that CI has the required dependency and that execution is authorized for M2.
Promotion: eligible only after artifact/run provenance and statistical checks.

## Alternative C — clean-room equivalence harness (diagnostic only)
Goal: validate data generation, metric schema, RAW/POST plumbing, and artifact writing without substituting a non-canonical LEACE implementation for the scientific run.

Advantages: can unblock infrastructure validation immediately without claiming LEACE evidence.
Risks: cannot answer the scientific M2 hypothesis; must remain EXPLORATORY/INFRASTRUCTURE.
Promotion: never as canonical LEACE evidence.

## Decision
Do not silently choose A or B on behalf of M*. A is scientifically preferred if the dependency can be provided reproducibly; B is preferred if the repository's controlled CI already defines the approved environment. C can proceed only as infrastructure validation and cannot generate a promoted M2 result.

## Publicability assessment
No current M4 execution is classified as a publishable M2 result. The canonical method is potentially publishable once an auditable run demonstrates the pre-specified effect with held-out evaluation, utility accounting, uncertainty, and falsification. The old P02 smoke output is explicitly not publishable as canonical LEACE evidence.
