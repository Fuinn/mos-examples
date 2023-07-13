#@ Model: Lasso
#@ Description: Machine Learning: Lasso Regression. Example from cvxpy.org/examples/machine_learning/lasso_regression.html  $$\min (\beta X - Y)+\lambda||\beta||$$ Find the regression coefficients (beta) that minimize the above regularized function

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import json

np.random.seed(1)

#@ Helper Object: m
#@ Description: number of data points
m = 100

#@ Helper Object: n
#@ Description: number of features
n = 20

#@ Helper Object: sigma
#@ Description: $$\sigma$$ parameter for generating random dataset
sigma = 5

#@ Helper Object: density
#@ Description: density parameter for generating random dataset
density = 0.2

#@ Helper Object: X
#@ Description: data matrix X
X = np.random.randn(m,n)


#@ Helper Object: Y
#@ Description: observations Y
beta_star = np.random.randn(n)
idxs = np.random.choice(range(n), int((1-density)*n), replace=False)
for idx in idxs:
    beta_star[idx] = 0
Y = X.dot(beta_star) + np.random.normal(0, sigma, size=m)

#@ Helper Object: X_train
#@ Description: training data
X_train = X[:50, :]

#@ Helper Object: Y_train
#@ Description: training observations
Y_train = Y[:50]

#@ Helper Object: X_test
#@ Description: test data
X_test = X[50:, :]

#@ Helper Object: Y_test
#@ Description: test observations
Y_test = Y[50:]


#@ Input Object: lambd
#@ Description: $$\lambda$$: regularization parameter
lambd = .1


#@ Variable: beta
#@ Description: $$\beta$$: regression coefficients
#@ Labels: labels_beta
beta = cp.Variable(n)

labels_beta = dict([(i, 'Feature %d' %i) for i in range(n)])

#@ Function: loss_fn
#@ Description: loss function $$\beta X_{train} - Y_{train}$$
loss_fn = cp.norm2(X_train @ beta - Y_train)**2

#@ Function: regularizer
#@ Description: regularization component of objective function $$||\beta||$$
regularizer = cp.norm1(beta)

#@ Function: objectivefn
#@ Description: objective function $$loss_{fn}+\lambda||\beta||$$
objectivefn = loss_fn + lambd * regularizer

#@ Problem: problem
problem = cp.Problem(cp.Minimize(objectivefn))

#@ Solver: solver
solver = "ECOS"

problem.solve(solver=solver, verbose=True)


#@ Helper Object: training_mse
#@ Description: training mean squared error
training_mse = (1.0 / X_train.shape[0]) * loss_fn.value

#@ Helper Object: testing_mse
#@ Description: testing mean squared error
testing_mse = (1.0 / X_test.shape[0]) * (cp.norm2(X_test @ beta.value - Y_test)**2).value

