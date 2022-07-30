#@ Model: Transportation
#@ Description: My first Pyomo transportation model from: https://pascua.iit.comillas.edu/aramos/simio/transpa/s_GoodOptimizationModelingPracticesPyomo.pdf

import pyomo.environ as pyo
from pyomo.environ import ConcreteModel, Set, Param, Var, NonNegativeReals, Constraint, Objective, minimize, Suffix
from pyomo.opt import SolverFactory

# Currently, the MOS Pyomo kernel requires 'model' as the keyword for a Concrete Model object
model = ConcreteModel('Transportation Problem')

#@ Helper Object: i
#@ Description: Origins
model.i = Set(initialize=['Vigo', 'Algeciras' ], doc='origins' )
#@ Helper Object: j
#@ Description: Destinations
model.j = Set(initialize=['Madrid', 'Barcelona', 'Valencia'], doc='destinations')

#@ Helper Object: pA
#@ Description: Origin capacity
model.pA = Param(model.i, initialize={'Vigo' : 350, 'Algeciras': 700 }, doc='origin capacity' )

#@ Helper Object: pA
#@ Description: Destination demand
model.pB = Param(model.j, initialize={'Madrid': 400, 'Barcelona': 450, 'Valencia': 150}, doc='destination demand')
TransportationCost = {
    ('Vigo', 'Madrid' ): 0.06,
    ('Vigo', 'Barcelona'): 0.12,
    ('Vigo', 'Valencia' ): 0.09,
    ('Algeciras', 'Madrid' ): 0.05,
    ('Algeciras', 'Barcelona'): 0.15,
    ('Algeciras', 'Valencia' ): 0.11,
 }

#@ Helper Object: pC
#@ Description: per unit transportation cost
model.pC = Param(model.i, model.j, initialize=TransportationCost, doc='per unit transportation cost')

#@ Variable: vX
#@ Description: units transported
model.vX = Var (model.i, model.j, bounds=(0.0,None), doc='units transported', within=NonNegativeReals)

#@ Constraint: eCapacity
#@ Description: maximum capacity of each origin
def eCapacity(model, i):
    return sum(model.vX[i,j] for j in model.j) <= model.pA[i]
model.eCapacity = Constraint(model.i, rule=eCapacity, doc='maximum capacity of each origin')

#@ Constraint: eDemand
#@ Description: demand supply at destination
def eDemand (model, j):
    return sum(model.vX[i,j] for i in model.i) >= model.pB[j]
model.eDemand = Constraint(model.j, rule=eDemand, doc='demand supply at destination' )

#@ Function: eCost
#@ Description: Objective function, transportation cost
def eCost(model):
    return sum(model.pC[i,j]*model.vX[i,j] for i,j in model.i*model.j)
model.eCost = Objective(rule=eCost, sense=minimize, doc='transportation cost')

model.write('model.lp', io_options={'symbolic_solver_labels': True})

model.dual = Suffix(direction=Suffix.IMPORT)

#@ Solver: solver
solver = 'cbc'


Solver = SolverFactory(solver)
Solver.options['LogFile'] = 'model.log'
#@ Problem: SolverResults
SolverResults = Solver.solve(model, tee=True)

SolverResults.write()
model.pprint()

model.vX.display()
for j in model.j:
    print(model.dual[model.eDemand[j]])
