# M4 independent test — results

## Execution
Independent synthetic validation completed locally from the M4 code path. The public `lab` CI then executed the same test suite successfully on GitHub Actions run 31826211053.

## Frozen synthetic setup
- seed: 42
- two protected groups: 300/300
- dimension: 12
- train/test split: 240/60 per group
- group shift injected in two coordinates
- targets: lambda = 0, .25, .5, .75, 1
- intervention: alpha = 0, .05, ..., 1
- primary target: lambda=.5

## Midpoint trajectory
| alpha | protected AUC | task macro-F1 | test mean gap | Gaussian symmetric KL |
|---:|---:|---:|---:|---:|
| 0.00 | 0.9447 | 0.7024 | 2.3911 | 3.2142 |
| 0.25 | 0.8858 | 0.7101 | 1.8168 | 1.9737 |
| 0.50 | 0.7914 | 0.7429 | 1.2554 | 1.0877 |
| 0.75 | 0.6531 | 0.7447 | 0.7366 | 0.5563 |
| 0.90 | 0.5611 | 0.7539 | 0.5042 | 0.4077 |
| 1.00 | 0.5000 | 0.7500 | 0.4476 | 0.3795 |

## Result
The midpoint intervention produces a smooth fairness improvement as alpha increases and also improves task macro-F1 in this synthetic construction. However, the predeclared interior-optimum criterion is **not supported** in this test: the best fairness point under a 0.005-F1 loss tolerance is alpha=1.0, not alpha<1.

Therefore this independent test supports the weaker claim:

> Moving both group means toward their midpoint can reduce linear protected predictability while preserving or improving utility in a controlled synthetic setting.

It does **not** support the stronger claim:

> An interior partial mean transport is generically optimal before full mean equalization.

## Gaussian interpretation
Symmetric diagonal-Gaussian KL falls from 3.2142 to 0.3795, but does not reach zero. Thus equalizing the means does not establish full distributional indistinguishability; covariance/shape differences remain.

## CI validation
The final public Actions test passed after resolving two harness issues: import path/package discovery and an invalid test assumption that test-set empirical means must equal the training-set target exactly. The corrected test checks exact equality on transformed training means and separately checks test-set improvement.

## Promotion status
`EXPLORATORY / INDEPENDENT VALIDATION`. No real-data claim is made from this synthetic run. The real-data MILK10k execution remains a separate gate.
