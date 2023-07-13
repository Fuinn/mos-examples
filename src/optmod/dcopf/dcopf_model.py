#@ Model: DCOPF Model
#@ Description: Sample DCOPF model in OPTMOD $$\min\sum_i (c_{0i}+c_{1i}P_{G_i}+c_{2i}P_{G_i}^2)$$$$P_{G}^{min}\leq P_{G}\leq P_{G}^{max}$$$$P_G-P_D=B\delta$$

import json
import pfnet
import optmod
import optalg

#@ Input File: case
#@ Description: Power flow case file
case = open('./src/optmod/dcopf/ieee14.m', 'r')

#@ Input Object: feastol
#@ Description: Feasibiltiy tolerance
feastol = 1e-4

#@ Helper Object: net
#@ Description: Power network data container
network = pfnet.Parser(case.name).parse(case.name)
net = json.loads(json.dumps(network, cls=pfnet.NetworkJSONEncoder))

#@ Variable: P
#@ Description: Generator active powers
#@ Labels: P_labels
P = optmod.VariableDict(name='P',
                        keys=[g.index for g in network.generators])

P_labels = {}
for g in network.generators:
    P_labels[g.index] = 'gen @ bus {}'.format(g.bus.number)

#@ Variable: w
#@ Description: Bus voltage angles
#@ Labels: w_labels
w = optmod.VariableDict(name='w',
                        keys=[bus.index for bus in network.buses])

w_labels = {}
for bus in network.buses:
    w_labels[bus.index] = 'v angle @ bus {}'.format(bus.number)

#@ Function: gen_cost
#@ Description: Generation cost function, objective function being minimized $$\sum_i (c_{0i}+c_{1i}P_{G_i}+c_{2i}P_{G_i}^2)$$
gen_cost = 0
for g in network.generators:
    gen_cost += g.cost_coeff_Q0 + g.cost_coeff_Q1*P[g.index] + g.cost_coeff_Q2*P[g.index]*P[g.index]

#@ Constraint: power_balance
#@ Description: Active power balance constraints $$P_G-P_D=B\delta$$
#@ Labels: pb_labels
power_balance = []
pb_labels = {}
for i, bus in enumerate(network.buses):
    dP = 0.
    for gen in bus.generators:
        dP += P[gen.index]
    for load in bus.loads:
        dP -= load.P
    for br in bus.branches_k:
        dP -= -br.b*(w[br.bus_k.index]-w[br.bus_m.index]-br.phase)
    for br in bus.branches_m:
        dP += -br.b*(w[br.bus_k.index]-w[br.bus_m.index]-br.phase)
    power_balance.append(dP == 0.)
    pb_labels[i] = 'P balance @ bus {}'.format(bus.number)

#@ Constraint: angle_ref
#@ Description: Voltage angle reference
#@ Labels: angle_ref_labels
i = 0
angle_ref = []
angle_ref_labels = {}
for bus in network.buses:
    if bus.is_slack():
        angle_ref.append(w[bus.index] == 0.)
        angle_ref_labels[i] = 'v angle @ bus {}'.format(bus.number)
        i += 1

#@ Constraint: P_limits
#@ Description: Generator active power limits $$P_{G_i}^{min}\leq P_{G_i}\leq P_{G_i}^{max}\quad\forall i$$
#@ Labels: P_limits_labels
P_limits = []
P_limits_labels = {}
for i, gen in enumerate(network.generators):
    P_limits.extend([P[gen.index] >= gen.P_min, P[gen.index] <= gen.P_max])
    P_limits_labels[2*i] = 'P_min gen @ bus {}'.format(gen.bus.number)
    P_limits_labels[2*i+1] = 'P_max gen @ bus {}'.format(gen.bus.number)

gen_cost_obj = optmod.minimize(gen_cost)

#@ Problem: problem
problem = optmod.Problem(gen_cost_obj,
                         constraints=power_balance+angle_ref+P_limits)

#@ Solver: solver
solver = optalg.opt_solver.OptSolverINLP()
solver.set_parameters({'feastol': feastol, 'maxiter': 100})

info = problem.solve(solver=solver)

#@ Output Object: output_obj
output_obj = list(info.values())

#@ Output File: output.txt
f = open('output.txt', 'w')
json.dump(info, f)
f.close()
