# Knapsack Model

A knapsack model implemented in JumP. This canonical model selects the most valuable items to place in a bag/knapsack, subject to the constraint that the full knapsack cannot exceed a weight/capacity limit. Many allocation problems across different industries may be formulated as knapsack problems.

$$\max p^T x$$

$$w^T x \leq k$$

$$x\in \\{0,1\\}^n $$


# Inputs

* `profit_file`: json file containing $p$ vector
* `weight`: $w$ vector
* `capacity`: capacity of knapsack, $k$


# Outputs

* `output.txt`: output file containing `x` vector, the choice of items (binary choice for each item)