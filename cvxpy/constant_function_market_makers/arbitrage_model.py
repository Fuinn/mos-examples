#@ Model: Constant Function Market Makers
#@ Description: Model adapted from https://github.com/angeris/cfmm-routing-code

import numpy as np
import cvxpy as cp

# Problem data
#@ Helper Object: global_indices
global_indices = list(range(4))
#@ Helper Object: local_indices
local_indices = [
    [0, 1, 2, 3],
    [0, 1],
    [1, 2],
    [2, 3],
    [2, 3]
]
#@ Helper Object: reserves
reserves = list(map(np.array, [
    [4, 4, 4, 4],
    [10, 1],
    [1, 5],
    [40, 50],
    [10, 10]
]))
#@ Helper Object: fees
fees = [
    .998,
    .997,
    .997,
    .997,
    .999
]
#@ Helper Object: market_value
#@ Description: "Market value" of tokens (say, in a centralized exchange)
market_value = [
    1.5,
    10,
    2,
    3
] 

# Build local-global matrices
#@ Helper Object: n
n = len(global_indices)
#@ Helper Object: m
m = len(local_indices)

#@ Helper Object: A
A = []
for l in local_indices:
    n_i = len(l)
    A_i = np.zeros((n, n_i))
    for i, idx in enumerate(l):
        A_i[idx, i] = 1
    A.append(A_i)

# Build variables
#@ Variable: deltas
#@ Labels: labels_locali
deltas = [cp.Variable(len(l), nonneg=True) for l in local_indices]
#@ Variable: lambdas
#@ Labels: labels_locali
lambdas = [cp.Variable(len(l), nonneg=True) for l in local_indices]

labels_locali = {}
for i,l in enumerate(local_indices):
    labels_locali[i] = dict([(j, 'L%d %d' % (i,k)) for j,k in enumerate(l)])

#@ Function: psi
#@ Description: coins out (objective function is to maximize the product of this function and 'market value')
psi = cp.sum([A_i @ (L - D) for A_i, D, L in zip(A, deltas, lambdas)])

# Objective is to maximize "total market value" of coins out
obj = cp.Maximize(market_value @ psi)

# Reserves after trade
#@ Function: new_reserves
#@ Labels: labels_locali
new_reserves = [R + gamma_i*D - L for R, gamma_i, D, L in zip(reserves, fees, deltas, lambdas)]

#@ Constraint: balancer_pool
#@ Description: Balancer pool with weights 4, 3, 2, 1
balancer_pool = cp.geo_mean(new_reserves[0], p=np.array([4, 3, 2, 1])) >= cp.geo_mean(reserves[0])

#@ Constraint: uniswap1
#@ Description: Uniswap v2 pools
uniswap1 = cp.geo_mean(new_reserves[1]) >= cp.geo_mean(reserves[1])

#@ Constraint: uniswap2
#@ Description: Uniswap v2 pools
uniswap2 = cp.geo_mean(new_reserves[2]) >= cp.geo_mean(reserves[2])

#@ Constraint: uniswap3
#@ Description: Uniswap v2 pools
uniswap3 = cp.geo_mean(new_reserves[3]) >= cp.geo_mean(reserves[3])

#@ Constraint: constant_sum_pool1
#@ Description: Constant sum pool
constant_sum_pool1 = cp.sum(new_reserves[4]) >= cp.sum(reserves[4])

#@ Constraint: constant_sum_pool2
#@ Description: Constant sum pool
constant_sum_pool2 = new_reserves[4] >= 0

#@ Constraint: arbitrage
#@ Description: Arbitrage constraint
arbitrage = psi >= 0


# Trading function constraints
cons = [
    balancer_pool,
    uniswap1,
    uniswap2,
    uniswap3,
    constant_sum_pool1,
    constant_sum_pool2,
    arbitrage]

# Set up and solve problem
#@ Problem: prob
prob = cp.Problem(obj, cons)
prob.solve(verbose=True)

print(f"Total output value: {prob.value}")


#@ Helper Object: output_value
#@ Description: Total output value
output_value = prob.value
