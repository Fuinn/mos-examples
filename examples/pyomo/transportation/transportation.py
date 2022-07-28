#@ Model: Transportation
#@ Description: My first Pyomo transportation model from: https://pascua.iit.comillas.edu/aramos/simio/transpa/s_GoodOptimizationModelingPracticesPyomo.pdf

import pyomo.environ as pyo
from pyomo.environ import ConcreteModel, Set, Param, Var, NonNegativeReals, Constraint, Objective, minimize, Suffix
from pyomo.opt import SolverFactory

mTransport = ConcreteModel('Transportation Problem')

#@ Helper Object: i
#@ Description: Origins
mTransport.i = Set(initialize=['Vigo', 'Algeciras' ], doc='origins' )
#@ Helper Object: j
#@ Description: Destinations
mTransport.j = Set(initialize=['Madrid', 'Barcelona', 'Valencia'], doc='destinations')

#@ Helper Object: pA
#@ Description: Origin capacity
mTransport.pA = Param(mTransport.i, initialize={'Vigo' : 350, 'Algeciras': 700 }, doc='origin capacity' )

#@ Helper Object: pA
#@ Description: Destination demand
mTransport.pB = Param(mTransport.j, initialize={'Madrid': 400, 'Barcelona': 450, 'Valencia': 150}, doc='destination demand')
TransportationCost = {
    ('Vigo', 'Madrid' ): 0.06,
    ('Vigo', 'Barcelona'): 0.12,
    ('Vigo', 'Valencia' ): 0.09,
    ('Algeciras', 'Madrid' ): 0.05,
    ('Algeciras', 'Barcelona'): 0.15,
    ('Algeciras', 'Valencia' ): 0.11,
 }

#@ Helper Object: pc
#@ Description: per unit transportation cost
mTransport.pC = Param(mTransport.i, mTransport.j, initialize=TransportationCost, doc='per unit transportation cost')

#@ Variable: vX
#@ Description: units transported
mTransport.vX = Var (mTransport.i, mTransport.j, bounds=(0.0,None), doc='units transported', within=NonNegativeReals)

#@ Constraint: eCapacity
#@ Description: maximum capacity of each origin
def eCapacity(mTransport, i):
    return sum(mTransport.vX[i,j] for j in mTransport.j) <= mTransport.pA[i]
mTransport.eCapacity = Constraint(mTransport.i, rule=eCapacity, doc='maximum capacity of each origin')

#@ Constraint: eDemand
#@ Description: demand supply at destination
def eDemand (mTransport, j):
    return sum(mTransport.vX[i,j] for i in mTransport.i) >= mTransport.pB[j]
mTransport.eDemand = Constraint(mTransport.j, rule=eDemand, doc='demand supply at destination' )

#@ Function: eCost
#@ Description: Objective function, transportation cost
def eCost(mTransport):
    return sum(mTransport.pC[i,j]*mTransport.vX[i,j] for i,j in mTransport.i*mTransport.j)
mTransport.eCost = Objective(rule=eCost, sense=minimize, doc='transportation cost')

mTransport.write('mTransport.lp', io_options={'symbolic_solver_labels': True})

mTransport.dual = Suffix(direction=Suffix.IMPORT)

#@ Solver: solver
solver = 'cbc'


Solver = SolverFactory(solver)
Solver.options['LogFile'] = 'mTransport.log'
#@ Problem: SolverResults
SolverResults = Solver.solve(mTransport, tee=True)

SolverResults.write()
mTransport.pprint()

mTransport.vX.display()
for j in mTransport.j:
    print(mTransport.dual[mTransport.eDemand[j]])
