# Knapsack Model

A knapsack model implemented in JumP. This canonical model 

$$\max p^T x$$

$$w^T x \leq k$$

$$x\in \\{0,1\\} $$


# Inputs

* `profit_file`: json file containing $p$ vector
* `weight`: $w$ vector
* `capacity`: capacity of knapsack, $k$


# Outputs

* `output.txt`: output file containing `x` vector, the choice of items