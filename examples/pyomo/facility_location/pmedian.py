#@ Model: Facility Location
#@ Description: Adapted from https://nbviewer.jupyter.org/github/Pyomo/PyomoGallery/blob/master/p_median/p_median.ipynb

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

import random

import json

random.seed(1000)

model = pyo.AbstractModel()

#@ Helper Object: m
#@ Description: Number of candidate locations
model.m = pyo.Param(within=pyo.PositiveIntegers)
#@ Helper Object: n
#@ Description: Number of customers
model.n = pyo.Param(within=pyo.PositiveIntegers)
#@ Helper Object: M
#@ Description: Set of candidate locations
model.M = pyo.RangeSet(1,model.m)
#@ Helper Object: N
#@ Description: Set of customer nodes
model.N = pyo.RangeSet(1,model.n)

#@ Helper Object: p
#@ Description: Number of facilities
model.p = pyo.Param(within=pyo.RangeSet(1,model.n))
#@ Helper Object: d
#@ Description: d[j] - demand of customer j
model.d = pyo.Param(model.N, default=1.0)
#@ Helper Object: c
#@ Description: c[i,j] - unit cost of satisfying customer j from facility i
model.c = pyo.Param(model.M, model.N, initialize=lambda i, j, model : random.uniform(1.0,2.0), within=pyo.Reals)

#@ Variable: x
#@ Description: x[i,j] - fraction of the demand of customer j that is supplied by facility i
#@ Labels: xlabels
model.x = pyo.Var(model.M, model.N, bounds=(0.0,1.0))

                
#@ Variable: y
#@ Description: y[i] - a binary value that is 1 is a facility is located at location i
#@ Labels: ylabels
model.y = pyo.Var(model.M, within=pyo.Binary)

#@ Function: cost
#@ Description: Minimize the demand-weighted total cost
def cost_(model):
    return sum(model.d[j]*model.c[i,j]*model.x[i,j] for i in model.M for j in model.N)
model.cost = pyo.Objective(rule=cost_)

#@ Constraint: demand
#@ Description: All of the demand for customer j must be satisfied
#@ Labels: ylabels
def demand_(model, j):
    return sum(model.x[i,j] for i in model.M) == 1.0
model.demand = pyo.Constraint(model.N, rule=demand_)

#@ Constraint: facilities
#@ Description: Exactly p facilities are located
def facilities_(model):
    return sum(model.y[i] for i in model.M) == model.p
model.facilities = pyo.Constraint(rule=facilities_)

#@ Constraint: openfac
#@ Description: Demand nodes can only be assigned to open facilities
#@ Labels: xlabels
def openfac_(model, i, j):
    return model.x[i,j] <= model.y[i]
model.openfac = pyo.Constraint(model.M, model.N, rule=openfac_)

#@ Input File: pmedian
#@ Description: input file with problem data
data = 'pmedian.dat'


#@ Solver: solver
solver = 'cbc'

opt = SolverFactory(solver)

# For now, we require instance to be the keyword here to be compatible with MOS Pyomo kernel
instance = model.create_instance(data)
instance.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
#@ Problem: facility
facility = opt.solve(instance)

print(facility)


# Define labels

xlabels = {}
for i in instance.M.data():
    for j in instance.N.data():
        xlabels[(i,j)] = 'fac. %d cust. %d' %(i, j)


ylabels = dict([(i, 'facility %d' %i) for i in instance.M.data()])

