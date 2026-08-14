# M3 LAB — LASSI / GLOW / MILK10k

Public programming laboratory for independent M3 experiments.

## Scope

This lab is intentionally independent from the private thesis record. It contains only code, environment specifications, reproducibility tooling, public-source references, synthetic smoke tests, and experiments that can safely be run without exposing unpublished thesis evidence.

It does **not** contain private datasets, private credentials, unpublished thesis conclusions, frozen private evidence, or the canonical manuscript.

## Scientific target

Test whether the LASSI/GLOW representation-learning approach can be technically reproduced and adapted to the MILK10k setting, before any result is promoted to the private research record.

MILK10k provides paired clinical and dermoscopic images plus metadata, including age, sex, skin tone, anatomical site and diagnosis. The official benchmark has 5,240 training lesions and 479 held-out test lesions, with 11 challenge diagnostic categories.

## Experiments

```text
M3-LG-00  environment / dependency smoke test
M3-LG-01  LASSI/GLOW code-path reproduction on synthetic data
M3-LG-02  representation extraction interface on MILK10k-format samples
M3-LG-03  GLOW counterfactual sanity checks: does changing Z also change Y-relevant content?
M3-LG-04  frozen-representation probes: Y predictability vs Z predictability
M3-LG-05  LASSI adaptation prototype
M3-LG-06  comparison against a non-generative representation baseline
```

## Data rule

The public lab references the official MILK10k source but does not redistribute the dataset. Obtain it directly from ISIC under its applicable licence/terms. The lab code must work from a local `MILK10k` path supplied at runtime.

## Independence rule

A lab experiment may be exploratory, negative, failed, anomalous or inconclusive. No experiment is considered thesis evidence merely because it runs successfully. Promotion requires an independent validation step in the private research record.

> Public lab = programming and reproducibility. Private repository = thesis evidence and scientific record.

## References

- LASSI: Peychev et al., ECCV 2022, *Latent Space Smoothing for Individually Fair Representations*.
- Official LASSI project: https://eth-sri.github.io/publications/peychev2022latent
- Official MILK10k Challenge: https://challenge.isic-archive.com/landing/milk10k/
- Official MILK10k data page: https://challenge.isic-archive.com/data/

## Status

`EXPLORATORY`
