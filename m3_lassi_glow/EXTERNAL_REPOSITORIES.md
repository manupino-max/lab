# M3 external repository inventory

This file records public repositories inspected for reusable programming ideas or reference implementations. It is not a claim that their code, weights or data are incorporated into M3.

| Source | Intended use | Status | Licence / terms rule |
|---|---|---|---|
| `eth-sri/lassi` | upstream LASSI implementation | inspect/download at runtime | verify upstream licence before redistribution |
| `Mametchiii/lassi-reproducibility` | independent reproduction and failure analysis | reference | use as scientific reference; do not copy without licence check |
| `daaviidmadrid/milk10k-fairness-skin-lesion-classification` | fairness protocol/code ideas | inspect | repository and dataset terms checked separately |
| `sshemanth/multimodal-lesion-diagnosis` | multimodal pipeline ideas | inspect | repository terms checked before reuse |
| `enjoeyland/PanDerm_milk10k` | foundation-model / MILK10k integration ideas | inspect | repository/model terms checked before reuse |
| `tech-doc/ConvNeXt_Milk10k` | optional pretrained baseline reference | inspect only | model card states CC BY-NC 4.0; no redistribution by default |
| `SaptarshiPani/MM-Skin-FS` | multimodal MILK10k baseline reference | inspect | code/data/weights treated separately |

## Acquisition rule

M3 may clone public repositories into the ephemeral Colab/CI runtime for inspection or execution. It must not silently vendor third-party source into the public M3 repository.

## Evidence rule

A successful execution of an external implementation is labelled `EXTERNAL_REPRODUCTION`, never `M3_RESULT`, until the protocol, environment, data provenance and independent validation requirements are satisfied.

## Dataset rule

MILK10k images are acquired from the official ISIC source under its applicable terms. Public mirrors may be used only as recovery/consistency checks and never silently replace the official source.
