# M4 Mean-Line / Gaussian Fairness

Primary hypothesis: moving both protected-group distributions toward the common midpoint of their empirical means can improve fairness before full erasure, while preserving utility.

For group means mu0 and mu1, target m(lambda)=lambda*mu0+(1-lambda)*mu1. Intervention: z'_g=z+alpha*(m(lambda)-mu_g), alpha in [0,1]. Primary lambda=0.5. Secondary lambda sweep: 0, .25, .5, .75, 1.

Gaussian interpretation is tested only as a diagnostic: diagonal-Gaussian symmetric KL between transformed group distributions. Equal means do not by themselves imply identical Gaussian distributions unless covariance is also equal; therefore covariance separation is retained as a falsification check.
