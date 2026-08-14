# M3 LAB — LASSI / GLOW / MILK10k

Public programming laboratory for independent M3 experiments.

## Purpose

This laboratory is deliberately independent from the private thesis record. It contains reproducible programming, public-source integration, synthetic tests, dataset-schema checks, and exploratory experiments. It does **not** contain private thesis data, credentials, unpublished conclusions, frozen private evidence, or the canonical manuscript.

The scientific target is to test whether LASSI/GLOW-style representation fairness can be adapted to MILK10k while preserving diagnostic information. This is an open question; the lab is allowed to fail.

## Run the full public lab

Google Colab can execute the public bootstrap from `colab/M3_COMPLETE_RUN.py`. It performs environment checks, downloads the public LASSI source at runtime, runs a synthetic representation probe, and, when an official MILK10k copy has been obtained locally, validates the dataset schema. Later stages are deliberately separated so that a failure in data acquisition does not become a fabricated scientific result.

## Experimental ladder

```text
M3-LG-00  environment / dependency smoke test
M3-LG-01  upstream LASSI source and reproducibility check
M3-LG-02  MILK10k acquisition/schema/integrity
M3-LG-03  public baseline representation
M3-LG-04  frozen feature extraction
M3-LG-05  Y task probe
M3-LG-06  Z sensitive-attribute probe
M3-LG-07  GLOW counterfactual validity
M3-LG-08  LASSI adaptation
M3-LG-09  fairness/utility comparison
M3-LG-10  comparator methods
M3-LG-11  robustness / seeds / modality checks
M3-LG-12  LAB_REPRODUCED candidate
```

## Key question

For representation `H = f(X)`, test whether sensitive information can be reduced while retaining diagnostic information: `Z -> H` predictability should decrease while `Y -> H` task performance remains acceptable.

The critical GLOW test comes before LASSI: a transformation intended to alter `Z` must be checked for unintended changes to diagnosis-relevant content. If that condition fails, the corresponding LASSI experiment is reported as invalid/inconclusive rather than forced through.

## Dataset and licence

MILK10k is the official ISIC 2025 dataset. The ISIC page states: 10,480 JPEG training images for 5,240 lesions, 10,480 metadata entries, supplemental metadata, and 5,240 diagnoses; the dataset is **CC BY-NC 4.0**. The public lab therefore does not redistribute the images. Obtain them directly from ISIC under the applicable terms.

Required dataset attribution:

> MILK study team. MILK10k. ISIC Archive, 2025. DOI: 10.34970/648456.

Dataset descriptor: Tschandl et al., Journal of Investigative Dermatology, 2026, DOI 10.1016/j.jid.2025.06.1594.

## External source policy

We may use public repositories for code/infrastructure/reference implementations, but each external component is provenance-tracked and licence-checked. Third-party model weights and datasets are never assumed to inherit the licence of the repository that hosts them.

Important external references currently investigated include the upstream LASSI implementation, MILK10k-specific models, multimodal MILK10k implementations, skin-tone fairness work, and GenAI fairness assessment on MILK10k. See `BIBLIOGRAPHY.bib` and `LICENSES_AND_SOURCES.md`.

## Scientific integrity

Public lab status values: `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED_BY_LICENSE`, `BLOCKED_BY_DATA`, `NOT_REPRODUCED`.

`PASS` means the computational stage passed its predefined test. It does not mean that a thesis hypothesis is confirmed.

A public lab result becomes thesis evidence only after independent validation in the private research record.

## Original code licence

Original M3 LAB code is MIT licensed in `LICENSE-M3-LAB`. This does not alter any third-party dataset, model, checkpoint, repository or paper terms.
