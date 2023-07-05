# Financial Portfolio Model
Sample portfolio optimization model in cvxpy. Example from https://colab.research.google.com/github/cvxgrp/cvx_short_course/blob/master/applications/portfolio_optimization.ipynb

# Overview

This model allocates a financial portfolio by maximizing expected return less risk, subject to a leverage constraint. Stock performance data is randomly generated in this sample example.

$$\max ret - \gamma risk$$

$$ret=\mu^T w$$

$$risk=Fw\Sigma+wD$$

$$\sum w = 1$$

$$||w||_1 \leq L$$



# Inputs

* `stockdata`: csv file with stock information - number of stocks to choose from, and number of factors
* `L`: leverage limit
* `gamma`: risk aversion parameter


# Outputs

* `output.txt`: output file containing `w` vector, the allocation of stocks
* `allocation.png`: plot displaying allocation of stocks