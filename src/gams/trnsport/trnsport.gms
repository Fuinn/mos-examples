*@ Model: Transportation Model
*@ Description: Sample transportation model in GAMS
$onText
This problem finds a least cost shipping schedule that meets
requirements at markets and supplies at factories.

Dantzig, G B, Chapter 3.3. In Linear Programming and Extensions.
Princeton University Press, Princeton, New Jersey, 1963.

This formulation is described in detail in:
Rosenthal, R E, Chapter 2: A GAMS Tutorial. In GAMS: A User's Guide.
The Scientific Press, Redwood City, California, 1988.

The line numbers will not match those in the book because of these
comments.

Keywords: linear programming, transportation problem, scheduling
$offText


*@ Helper Object: i
*@ Description: canning plants
Set i 'canning plants' / seattle,  san-diego /   ;

*@ Helper Object: j
*@ Description: markets
Set j 'markets'        / new-york, chicago, topeka /;

*@ Helper Object: a
*@ Description: capacity of plant i
Parameter  a(i) 'capacity of plant i in cases' 
        / seattle    350
          san-diego  600 /;

*@ Helper Object: b
*@ Description: demand at market j
Parameter  b(j) 'demand at market j in cases'
        / new-york   325
          chicago    300
          topeka     275 /;

*@ Input File: d
*@ Description: distance betwen cities
$include 'd.inc'

*@ Input Object: f
*@ Description: freight costs
Scalar f 'freight in dollars per case per thousand miles' / 90 /;

*@ Function: c
*@ Description: transport costs
Parameter c(i,j) 'transport cost in thousands of dollars per case';
c(i,j) = f*d(i,j)/1000;

*@ Variable: x
*@ Description: shipment quantities
Positive Variable  x(i,j) 'shipment quantities in cases';

*@ Variable: z
*@ Description: total transportation costs
Variable   z      'total transportation costs in thousands of dollars';


*@ Constraint: cost
*@ Description: define variable to be minimized
Equation  cost      'define objective function';
cost..      z =e= sum((i,j), c(i,j)*x(i,j));

*@ Constraint: supply
*@ Description: observe supply limit at plant i
Equation   supply(i) 'observe supply limit at plant i';
supply(i).. sum(j, x(i,j)) =l= a(i);

*@ Constraint: demand
*@ Description: satisfy demand at market j
Equation  demand(j) 'satisfy demand at market j';
demand(j).. sum(i, x(i,j)) =g= b(j);

*@ Problem: transport
Model transport / all /;


*@ Solver: solver
parameter solver(*);

solve transport using lp minimizing z;

display x.l, x.m, transport.solveStat,transport.objVal,transport.iterUsd;

solver('objective') = transport.objVal;
solver('status') = transport.solveStat;
solver('iterations') = transport.iterUsd;
solver('time') = transport.etSolver;

*@ Output File: results.txt
File results /results.txt/;
put results;
put 'Model Results' / / ;
loop((i,j), put i.tl, @12, j.tl, @24, x.l(i,j):8:4 /);

*@ Output File: output.gdx
execute_unload 'output.gdx';

*@ Output Object: marginal
parameter marginal;
marginal("supply",i) = supply.m(i);