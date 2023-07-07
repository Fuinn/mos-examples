# Lasso Regression
Machine Learning: Lasso Regression. Example from https://www.cvxpy.org/examples/machine_learning/lasso_regression.html



# Overview


Finds the regression coefficients ($\beta$) that minimize the following regularized function:

$$\min (\beta X - Y)+\lambda||\beta||$$



# Inputs

* `stockdata`: csv file with stock information - number of stocks to choose from, and number of factors
* `L`: leverage limit
* `gamma`: risk aversion parameter


# Outputs

* `output.txt`: output file containing `w` vector, the allocation of stocks
* `allocation.png`: plot displaying allocation of stocks