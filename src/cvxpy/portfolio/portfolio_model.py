#@ Model: Portfolio Model
#@ Description: Sample portfolio optimization model in cvxpy. Example from https://colab.research.google.com/github/cvxgrp/cvx_short_course/blob/master/applications/portfolio_optimization.ipynb $$\max ret - \gamma risk$$$$ret=\mu^T w$$$$risk=Fw\Sigma+wD$$$$\sum w = 1$$$$||w||_1 \leq L$$

import numpy as np
import cvxpy as cp
import json
import matplotlib.pyplot as plt
import csv

#@ Input File: stockdata
#@ Description: input file with data on stocks and factors
stockdata = open('./src/cvxpy/portfolio/stockdata.csv','r')
row1 = next(csv.reader(stockdata))

#@ Helper Object: n
#@ Description: number of portfolio members to choose from
n = int(row1[0])

#@ Helper Object: m
#@ Description: number of factors
m = int(row1[1])

#@ Input Object: gamma
#@ Description: Risk aversion parameter
gamma = 0.1

#@ Input Object: L
#@ Description: Leverage limit
L = 2

#@ Helper Object: mu
#@ Description: Expected return of a stock
mu = np.abs(np.random.randn(n, 1))

#@ Helper Object: Sigma_tilde
#@ Description: Factor covariance matrix
Sigma_tilde = np.random.randn(m, m)
Sigma_tilde = Sigma_tilde.T.dot(Sigma_tilde)

#@ Helper Object: D
#@ Description: Diagonal matrix of idiosyncratic risks
D = np.diag(np.random.uniform(0, 0.9, size=n))

#@ Helper Object: F
#@ Description: Factor loading matrix
F = np.random.randn(n, m)

#@ Variable: w
#@ Description: Portfolio allocation vector
#@ Labels: labels_w
w = cp.Variable(n)

labels_w = dict([(i, 'Stock %d' %i) for i in range(n)])

#@ Function: ret
#@ Description: Expected return on portfolio $$\mu^T w$$
ret = mu.T*w

#@ Function: risk
#@ Description: Risk of portfolio, related to variance $$risk=Fw\Sigma+wD$$
risk = cp.quad_form(F.T*w, Sigma_tilde) + cp.quad_form(w, D)

#@ Function: objectivefn
#@ Description: objective function : return less risk$$ret - \gamma risk$$
objectivefn = ret - gamma*risk

#@ Constraint: Allocation
#@ Description: sum of fractional allocations must equal 1 $$\sum w = 1$$
Allocation = cp.sum(w) == 1

#@ Constraint: Leverage
#@ Description: leverage limit constraint, allows us to have some negative w (i.e. we can borrow shares) $$||w||_1 \leq L$$
Leverage = cp.norm(w, 1) <= L 

#@ Problem: prob_factor
constraints = []
constraints.append(Allocation)
constraints.append(Leverage)

prob_factor = cp.Problem(cp.Maximize(objectivefn), constraints)

#@ Solver: solver
solver = "ECOS"

prob_factor.solve(solver=solver, verbose=True)

#@ Helper Object: display
#@ Description: Display output in human readable form
display = []
labels = []
count = 0
for item in w.value:
    if abs(item) > 0.01:
        display.append([count,item])
        labels.append(str(count))
    count += 1

#@ Output File: output.txt
outfile = open('output.txt','w')
json.dump(display,outfile)
outfile.close()


#@ Output File: allocation.png
fig = plt.figure()
plt.bar(np.arange(len(labels)),100*np.array(display)[:,1],tick_label=labels)
#plt.xticks(np.arange(len(labels)), labels)
#plt.pie(np.array(display)[:,1], labels=labels, autopct='%1.1f%%')
#plt.pie(w.value, labels=np.arange(n), autopct='%1.1f%%')
#plt.axis('equal')
plt.xlabel('stock selected')
plt.ylabel('allocation %')
plt.savefig('allocation.png')
