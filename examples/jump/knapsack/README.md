# Knapsack Model

Sample knapsack model in JumP.

$$\max p^T x$$

$$w^T x \leq k$$

$$x\in\{0,1\}$$


# Inputs

* `stockdata`: csv file with stock information - number of stocks to choose from, and number of factors
* `L`: leverage limit
* `gamma`: risk aversion parameter


# Outputs

* `output.txt`: output file containing `w` vector, the allocation of stocks
* `allocation.png`: plot displaying allocation of stocks