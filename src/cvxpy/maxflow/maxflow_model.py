#@ Model: Max flow
#@ Description: Model to find maximum flow across a network $$\max x_{50}$$$$\sum_k x_{ki}=\sum_j x_{ij},\quad\forall i$$$$0 \leq x_{ij} \leq k_{ij},\quad\forall i,j$$

import cvxpy as cp
import numpy as np
import json


#@ Helper Object: k
#@ Description: Capacity of edges
k = [[0,6,11,0,0,0],[0,0,0,12,5,0],[0,0,0,0,10,0],[0,0,0,0,0,13],[0,5,0,0,0,4],[1e9,0,0,0,0,0]]
k = np.array(k)

#@ Variable: x
#@ Description: flow along each edge $$x\in\mathbb{r}^{6 \times 6}$$
#@ Labels: edges
x = cp.Variable((6,6))

edges = dict([((i,j), 'Edge %d %d' %(i, j)) for i in range (6) for j in range(6)])


#@ Function: objectivefn
#@ Description: $$x_{50}$$
objectivefn = x[5][0]

#@ Constraint: nodalbalance
#@ Description: Nodal balance, flows entering equal flows exiting at each node $$\sum_k x_{ki} = \sum_j x_{ij},\quad\forall i$$
#@ Labels: nodes
nodalbalance = cp.sum(x,axis=0) == cp.sum(x,axis=1)

nodes = dict([(i, 'Node %d' %i) for i in range(6)])

#@ Constraint: x_upperbound
#@ Description: Capacity limit on each edge $$x \leq k$$
#@ Labels: edges
x_upperbound = x <= k

#@ Constraint: x_lowerbound
#@ Description: $$x \geq 0$$
#@ Labels: edges
x_lowerbound = x >= 0


#@ Problem: allocation
constraints = []
constraints.append(nodalbalance)
constraints.append(x_upperbound)
constraints.append(x_lowerbound)


allocation = cp.Problem(cp.Maximize(objectivefn), constraints)

#@ Solver: solver
solver = "ECOS"


allocation.solve(solver=solver, verbose=True, abstol=2e-3)

