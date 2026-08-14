"""M4: mean-line / Gaussian fairness intervention.

For group means mu0, mu1, define m(lambda)=lambda*mu0+(1-lambda)*mu1.
Each group is translated along the line [mu0,mu1] toward m(lambda):
    z'_g = z + alpha*(m(lambda)-mu_g), alpha in [0,1].
The primary target is lambda=.5 (the midpoint / common fairness mean).
The experiment also sweeps lambda to test whether another convex combination
is preferable and reports a diagonal-Gaussian symmetric-KL diagnostic.
"""

# Canonical implementation lives in .github/workflows/m4_mean_line_gaussian_fairness.yml
# so the frozen real-data run is reproducible in GitHub Actions.
