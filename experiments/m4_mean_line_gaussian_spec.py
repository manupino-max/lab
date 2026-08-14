EXPERIMENT_ID = 'M4_MEAN_LINE_GAUSSIAN'
ALPHAS = [i / 20 for i in range(21)]
TARGET_LAMBDAS = [0.0, 0.25, 0.5, 0.75, 1.0]
# z'_g = z + alpha * (m(lambda) - mu_g)
# m(lambda) = lambda*mu0 + (1-lambda)*mu1
# lambda=.5 is the symmetric common fairness mean.
