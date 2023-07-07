# Transportation Assignment
Model to find minimum cost assignment between warehouses and retailers, given supply and demand constraints.



# Overview

$$\min \sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}$$

$$\sum_{j=1}^m x_{ij}=s_i,\quad\forall i=1,2,\dots,m$$

$$\sum_{i=1}^n x_{ij}=d_j,\quad\forall j=1,2,\dots,n$$

$$x_{ij}\geq 0 \quad\forall i,j$$ 



# Inputs

* $\lambda$: regularization parameter
* Feature and target data, $X$ and $Y$, are randomized in this example


# Outputs

* Regression coefficients $\beta$
* Training and testing Mean Square Errors (MSE)