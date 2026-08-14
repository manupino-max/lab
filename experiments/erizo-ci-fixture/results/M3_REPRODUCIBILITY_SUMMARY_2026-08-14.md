# M3 reproducibility summary — 2026-08-14

## Closed evidence
A frozen public synthetic ERIZO fixture was independently inspected from CI artifacts for Python 3.10 and 3.11. Both jobs succeeded; both verified 64 rows; both uploaded artifacts with identical archive SHA-256. The extracted CSV payloads are byte-for-byte identical and have identical payload SHA-256.

## Scientific boundary
This result supports reproducibility of the public fixture only. It does not support claims about real-data performance, fairness efficacy, LASSI efficacy, ERIZO scientific efficacy, or E8/E12.

## E8/E12 status
Still evidence-gated. Three routes remain prepared:
A. historical replay;
B. convergence-safe replay;
C. provenance-first E12.

## Project coordination
M3 has reported the publicability candidates to M*. The current high-value candidate is a reproducible historical-vs-convergence methodological discrepancy if A/B demonstrates an interpretation-changing effect. A provenance/metric discrepancy in E12 is a secondary candidate. Both remain hypotheses about possible findings, not results.
