
#@ Model: Transportation Assignment
#@ Description: Model to find minimum cost assignment between warehouses and retailers, given supply and demand constraints $$\min \sum_{i=1}^{3}\sum_{j=1}^{4}c_{ij}x_{ij}$$$$\sum_{j=1}^4 x_{ij}=s_i,\quad\forall i=1,2,3$$$$\sum_{i=1}^3 x_{ij}=d_j,\quad\forall j=1,2,3,4$$$$x_{ij}\geq 0 \quad\forall i,j$$

import cvxpy as cp
import json

#@ Input Object: s
#@ Description: Supply from each warehouse
s = [500,700,800]

#@ Input Object: d
#@ Description: Demand from each retailer
d = [400,900,200,500]

#@ Input Object: c
#@ Description: Matrix of costs
c = [[12,13,4,6],[6,4,10,11],[10,9,12,14]]

#@ Variable: x
#@ Description: Assignment from warehouse i to retailer j (non-negative)
#@ Labels: x_labels
x = cp.Variable((3,4), nonneg=True)

warehouse = ['A', 'B', 'C']
retailer = ['W', 'X', 'Y', 'Z']
x_labels = {}
for i in range(3):
    for j in range(4):
        x_labels[(i,j)] = '{} to {}'.format(warehouse[i], retailer[j])

#@ Function: objectivefn
#@ Description: Costs (minimize) $$\sum_{i=1}^3\sum_{j=1}^4 c_{ij}x_{ij}$$
objectivefn = cp.sum(cp.multiply(c,x.T))

#@ Constraint: supply
#@ Description: $$\sum_{j=1}^3 x_{ij} = s_i,\quad\forall i=1,2,3$$
#@ Labels: supply_labels
supply = cp.sum(x, axis=1) == s

supply_labels = {}
for i in range(3):
    supply_labels[i] = 'supply warehouse {}'.format(warehouse[i])
    
#@ Constraint: demand
#@ Description: $$\sum_{i=1}^4 x_{ij} = d_j,\quad\forall j=1,2,3,4$$
#@ Labels: demand_labels
demand = cp.sum(x, axis=0) == d

demand_labels = {}
for j in range(4):
    demand_labels[j] = 'demand retailer {}'.format(retailer[j])

#@ Problem: assignment
constraints = []
constraints.append(supply)
constraints.append(demand)

assignment = cp.Problem(cp.Minimize(objectivefn), constraints)


#@ Solver: solver
solver = "ECOS"


assignment.solve(solver=solver, verbose=True)



