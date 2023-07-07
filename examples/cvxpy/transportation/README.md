# Transportation Assignment
Model to find minimum cost assignment between warehouses and retailers, given supply and demand constraints.



# Overview

$$\min \sum_{i=1}^{3}\sum_{j=1}^{4}c_{ij}x_{ij}$$

$$\sum_{j=1}^4 x_{ij}=s_i,\quad\forall i=1,2,3$$

$$\sum_{i=1}^3 x_{ij}=d_j,\\ quad\forall j=1,2,3,4$$

$$x_{ij}\geq 0 \quad\forall i,j$$ 



# Inputs

* $\lambda$: regularization parameter
* Feature and target data, $X$ and $Y$, are randomized in this example


# Outputs

* Regression coefficients $\beta$
* Training and testing Mean Square Errors (MSE)