# M3 complete public LAB protocol

## Objective

Determine whether LASSI/GLOW-style representation fairness can be technically adapted to MILK10k while preserving diagnostic information. The experiment is deliberately exploratory and independent from the private thesis record.

## Core question

Can information about a selected sensitive attribute Z be reduced in a representation H while retaining predictive information for diagnosis Y?

## Stages

### E0 — Environment
- Python and dependency versions.
- CPU/GPU/CUDA inventory.
- upstream source commit hashes.

### E1 — Source reproduction
- Download upstream LASSI implementation at runtime.
- Record commit SHA and licence.
- Run its own available smoke/tests where feasible.

### E2 — MILK10k acquisition and integrity
- Obtain data only from official ISIC source.
- Validate 10,480 training images and 5,240 lesion identifiers.
- Verify metadata/diagnosis joins.
- Never split paired images independently.
- Keep lesion-level grouping intact.

### E3 — Public baseline
Run at least one independently reproducible pretrained/fine-tuned representation baseline. Candidate: dual-image ConvNeXt MILK10k model, subject to licence/terms. Record exact checkpoint identifier; do not redistribute it unless permitted.

### E4 — Representation extraction
Extract frozen representations H for clinical, dermoscopic and fused inputs where supported.

### E5 — Task probe
Estimate how well H predicts Y. Report macro-F1, balanced accuracy and per-class F1. Use lesion-level splits and keep test data isolated.

### E6 — Sensitive-attribute probe
For each available Z (starting with skin tone), estimate predictability from H using a fixed probe family. Report AUC/balanced accuracy and confidence intervals where feasible.

### E7 — GLOW/counterfactual validity
Before LASSI, test whether generated transformations intended to alter Z preserve diagnostic information. Compare original/generated pairs using task predictions, embedding distance and label consistency. A failure is a scientific result and blocks the LASSI adaptation for that transformation.

### E8 — LASSI adaptation
Only after E7 passes for a defined transformation family, implement an adaptation around the upstream method. Keep the original method distinguishable from our adapter.

### E9 — Fairness/performance trade-off
Compare RAW baseline vs LASSI/GLOW adaptation. Report both utility and sensitive-attribute leakage. Do not select hyperparameters using the held-out test set.

### E10 — Comparator methods
Where implementations are safely reusable, evaluate a common protocol against LEACE and other representation/fairness baselines. Every comparator gets its own provenance and licence record.

### E11 — Robustness
Repeat across seeds and, where computationally feasible, across representation backbones/modalities. Report failures and negative results.

### E12 — Freeze candidate result
Only a fully reproducible public LAB run may be marked `LAB_REPRODUCED`. It is **not** `THESIS_VALIDATED` until independently audited in the private research record.

## Non-negotiable anti-leakage rules

1. Split at lesion level.
2. Clinical and dermoscopic views from one lesion never cross train/validation/test boundaries.
3. No test labels used for training or hyperparameter selection.
4. No private thesis outputs copied into LAB.
5. External results are cited, not claimed as ours.
6. Failed runs remain discoverable through run manifests; they are not silently deleted.

## Outcome classes

`PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED_BY_LICENSE`, `BLOCKED_BY_DATA`, `NOT_REPRODUCED`.

A `PASS` means the computational stage passed its predefined test; it does not mean the scientific hypothesis was confirmed.
