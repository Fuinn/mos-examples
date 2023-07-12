#@ Model: Simple educational model
#@ Description: $$\min x+y$$ $$x\geq -1$$ $$y \geq 3$$ $$x\in\{0,1\}, y\in\mathbb{R}$$

# James Merrick, July 2020

import cvxpy as cvx
import numpy as np
import json


#set up problem


#@ Variable: x
#@ Description: \(x\in \{0,1\}\)
x = cvx.Variable(boolean=True)

#@ Variable: y
#@ Description: $$y\in \mathbb{R}$$
y = cvx.Variable()

#@ Function: objectivefn
#@ Description: objective function to minimize $$f(x,y)=x+y$$
objectivefn = cvx.sum(x+y)


#@ Constraint: xbound
#@ Description: $$x\geq -1$$
xbound = x >= -1

#@ Constraint: ybound
#@ Description: $$y\geq 3$$
ybound = y >= 3


#@ Problem: simple
constraints = []
constraints.append(xbound)
constraints.append(ybound)

objective = cvx.Minimize(objectivefn)
simple = cvx.Problem(objective, constraints)

#@ Solver: solver_simple
solver_simple = "ECOS_BB"


simple.solve(solver=solver_simple, verbose=True)


