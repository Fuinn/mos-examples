# Lasso Regression
Machine Learning: Lasso Regression. Example from https://www.cvxpy.org/examples/machine_learning/lasso_regression.html



# Overview


Given feature data $X$ and target data $Y$, this model finds the regression coefficients ($\beta$) that minimize the following regularized function:

$$\min (\beta X - Y)+\lambda||\beta||$$



# Inputs

* $\lambda$: regularization parameter
* Feature and target data, $X$ and $Y$, are randomized in this example


# Outputs

* Regression coefficients $\beta$
* Training and testing Mean Square Errors (MSE)