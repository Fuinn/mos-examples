#@ Model: ACOPF Model
#@ Description: Sample ACOPF model in OPTMOD

import json
import pfnet
import optmod
import optalg
from optmod import VariableDict, Problem, minimize, cos, sin

#@ Input File: case
#@ Description: Power flow case file
case = open('./examples/optmod/acopf/ieee14.m', 'r')

#@ Input Object: feastol
#@ Description: Feasibiltiy tolerance
feastol = 1e-4

#@ Helper Object: net_pre
#@ Description: Initial power network 
net = pfnet.Parser(case.name).parse(case.name)
net_pre = json.loads(json.dumps(net, cls=pfnet.NetworkJSONEncoder))

#@ Helper Object: gen_indices
#@ Description: Generator indices
gen_indices = [gen.index for gen in net.generators]

#@ Helper Object: P0
#@ Description: Initial generator active powers
P0 = dict([(gen.index, gen.P) for gen in net.generators])

#@ Helper Object: Q0
#@ Description: Initial generator reactive powers
Q0 = dict([(gen.index, gen.Q) for gen in net.generators])

#@ Helper Object: bus_indices
#@ Description: Bus indices
bus_indices =[bus.index for bus in net.buses]

#@ Helper Object: w0
#@ Description: Initial bus voltage angles
w0 = dict([(bus.index, bus.v_ang) for bus in net.buses])

#@ Helper Object: v0
#@ Description: Initial bus voltage magnitudes
v0 = dict([(bus.index, bus.v_mag) for bus in net.buses])

#@ Variable: P
#@ Description: Generator active powers
#@ Labels: Gen_labels
P = VariableDict(gen_indices, name='P', value=P0)

Gen_labels = {}
for g in net.generators:
    Gen_labels[g.index] = 'gen @ bus {}'.format(g.bus.number)

#@ Variable: Q
#@ Description: Generator reactive powers
#@ Labels: Gen_labels
Q = VariableDict(gen_indices, name='Q', value=Q0)

#@ Variable: w
#@ Description: Bus voltage angles
#@ Labels: w_labels
w = VariableDict(bus_indices, name='vang', value=w0)

w_labels = {}
for bus in net.buses:
    w_labels[bus.index] = 'v angle @ bus {}'.format(bus.number)


#@ Variable: v
#@ Description: Bus voltage magnitudes
#@ Labels: v_labels
v = VariableDict(bus_indices, name='vmag', value=v0)

v_labels = {}
for bus in net.buses:
    v_labels[bus.index] = 'v mag @ bus {}'.format(bus.number)


#@ Constraint: pbc
#@ Description: AC power balance constraint $$\delta P=0,\quad \delta Q=0$$

pbc = []

for bus in net.buses:
    dP = 0.
    dQ = 0.
    for gen in bus.generators:
        dP += P[gen.index]
        dQ += Q[gen.index]
    for load in bus.loads:
        dP -= load.P
        dQ -= load.Q
    for shunt in bus.shunts:
        dP -= shunt.g*v[bus.index]*v[bus.index]
        dQ += shunt.b*v[bus.index]*v[bus.index]
    for br in bus.branches_k:
        vk, vm = v[br.bus_k.index], v[br.bus_m.index]
        dw = w[br.bus_k.index]-w[br.bus_m.index]-br.phase
        dP -= (br.ratio**2.)*vk*vk*(br.g_k+br.g) - br.ratio*vk*vm*(br.g*cos(dw) + br.b*sin(dw))
        dQ -= -(br.ratio**2.)*vk*vk*(br.b_k+br.b) - br.ratio*vk*vm*(br.g*sin(dw) - br.b*cos(dw))
    for br in bus.branches_m:
        vk, vm = v[br.bus_k.index], v[br.bus_m.index]
        dw = w[br.bus_m.index]-w[br.bus_k.index]+br.phase
        dP -= vm*vm*(br.g_m+br.g) - br.ratio*vm*vk*(br.g*cos(dw) + br.b*sin(dw))
        dQ -= -vm*vm*(br.b_m+br.b) - br.ratio*vm*vk*(br.g*sin(dw) - br.b*cos(dw))
    pbc.extend([dP == 0., dQ == 0.])
    assert(abs(dP.get_value()-bus.P_mismatch) < 1e-8)
    assert(abs(dQ.get_value()-bus.Q_mismatch) < 1e-8)

#@ Constraint: plim
#@ Description: Generator active power limits $$P_G^{min}\leq P_G\leq P_G^{max}$$
plim = []
for gen in net.generators:
    plim.extend([gen.P_min <= P[gen.index], gen.P_max >= P[gen.index]])

#@ Constraint: qlim
#@ Description: Generator reactive power limits $$Q_G^{min}\leq Q_G\leq Q_G^{max}$$
qlim = []
for gen in net.generators:
    qlim.extend([gen.Q_min <= Q[gen.index], gen.Q_max >= Q[gen.index]])

#@ Constraint: vlim
#@ Description: Bus voltage magnitude limits $$V^{min}\leq V\leq V^{max}$$
vlim = []
for bus in net.buses:
    vlim.extend([bus.v_min <= v[bus.index], bus.v_max >= v[bus.index]])

#@ Constraint: wref
#@ Description: Bus voltage angle reference
wref = []
for bus in net.buses:
    if bus.is_slack():
        wref.append(w[bus.index] == bus.v_ang)

#@ Function: gen_cost
#@ Description: Generation cost function, objective function being minimized $$\sum_i (c_{0i}+c_{1i}P_{G_i}+c_{2i}P_{G_i}^2)$$
gen_cost = 0
for g in net.generators:
    gen_cost += (g.cost_coeff_Q0 + 
                 g.cost_coeff_Q1*P[g.index] + 
                 g.cost_coeff_Q2*P[g.index]*P[g.index])

#@ Problem: acopf
acopf = Problem(minimize(gen_cost), pbc+plim+qlim+vlim+wref)

#@ Solver: solver
solver = optalg.opt_solver.OptSolverINLP()
solver.set_parameters({'feastol': feastol, 'maxiter': 100})

info = acopf.solve(solver=solver)

#@ Helper Object: net_post
#@ Description: Optimized power network 
for bus in net.buses:
    bus.v_mag = v[bus.index].get_value()
    bus.v_ang = w[bus.index].get_value()
for gen in net.generators:
    gen.P = P[gen.index].get_value()
    gen.Q = Q[gen.index].get_value()
net.update_properties()
net_post = json.loads(json.dumps(net, cls=pfnet.NetworkJSONEncoder))

#@ Output Object: net_props
#@ Description: Container of solved network properties
net_props = net.get_properties()

#@ Output Object: branch_flows
#@ Description: Container of branch apparent power flows
branch_flows = {}
for br in net.branches:
    branch_flows[str((br.bus_k.number, br.bus_m.number))] = br.get_S_km_mag()


