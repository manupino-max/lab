# M3 LAB — licences, attribution and source policy

## Rule

We reuse public **code and ideas**, not third-party datasets or weights by default. Every external component must be identified before execution and its licence/terms recorded.

## Primary dataset

MILK10k is distributed by ISIC under **CC BY-NC 4.0**. The official ISIC page states that the training set contains 10,480 JPEG images for 5,240 lesions, plus metadata and diagnoses, and explicitly requires citation of the MILK study team dataset record. We therefore do not commit the images to this public repository and require direct acquisition from ISIC under the applicable terms.

Required attribution:

> MILK study team. MILK10k. ISIC Archive, 2025. DOI: 10.34970/648456.

Dataset descriptor:

> Tschandl et al. MILK10k: A Hierarchical Multimodal Imaging-Learning Toolkit for Diagnosing Pigmented and Nonpigmented Skin Cancer and its Simulators. Journal of Investigative Dermatology, 2026. DOI: 10.1016/j.jid.2025.06.1594.

## LASSI

LASSI is an external research method. The lab downloads the upstream implementation at runtime rather than copying it into this repository. We retain the upstream URL, commit/version used, paper citation and licence information in each run manifest.

## External MILK10k models/repositories

External implementations are treated as references or optional runtime dependencies. We do not redistribute their checkpoints unless their licence explicitly permits it. A model trained on MILK10k may inherit the dataset's non-commercial constraints; this must be checked before redistribution or commercial use.

Examples investigated for M3 include:

- `tech-doc/ConvNeXt_Milk10k` — pretrained dual ConvNeXt model; its model card states CC BY-NC 4.0 and non-commercial research use.
- Watanabe et al. 2026 — fairness assessment of skin-lesion classifiers using GenAI synthesis and MILK10k as a real-image benchmark.
- Ansari et al. 2024 — skin-tone bias mitigation in lesion classification.
- Pani et al. 2026 — multimodal skin-lesion classification including MILK10k.

## No licence laundering

An MIT/Apache/GPL licence on a GitHub repository does not automatically grant rights over datasets, pretrained weights, or third-party files contained in that repository. M3 records component-level provenance and treats dataset/weight terms separately.

## Thesis integrity

Public LAB outputs are exploratory/reproducibility evidence. They do not become thesis evidence automatically. No private thesis data, unpublished conclusions, credentials or frozen private records are committed here.
