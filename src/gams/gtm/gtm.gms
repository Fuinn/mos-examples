*@ Model: An International Gas Trade Model
*@ Description: Manne, A S, and Beltramo, M A, GTM: An International Gas Trade Model , International Energy Program Report. Stanford University, 1984.

$onText
The Gas Trade Model (GTM) models interrelated gas markets.
Prices may be free to move as to equilibrate supplies and
demand. Disequilibria can be introduced with controls over
prices and/or quantities traded.

Keywords: nonlinear programming, gas trade, price elasticity, energy economics,  international trade
$offText


*@ Input File: gtm_data
*@ Description: data for problem
$gdxin gtm_data.gdx

*@ Helper Object: i
*@ Description: supply regions
Set  i;
$load i

*@ Helper Object: j
*@ Description: demand regions
Set  j;
$load j

*@ Helper Object: jfx
*@ Description: regions with fixed demand
Set jfx(j)
$load jfx



*@ Helper Object: sdat
*@ Description: supply data
Parameter sdat(i,*);
$load sdat

*@ Helper Object: ddat
*@ Description: demand data
Parameter ddat(j,*);
$load ddat


*@ Helper Object: utc
*@ Description: unit transport cost ($ per mcf)
Parameter utc(i,j);
$load utc


*@ Helper Object: pc
*@ Description: pipeline capacities (tcf)
Parameter pc(i,j);
$load pc

*@ Helper Object: ij
*@ Description: feasible links
Set ij(i,j) ;
ij(i,j)     = yes$pc(i,j);


*@ Helper Object: check1
*@ Description: supply links with zero cost and non-zero capacity
Set check1(i,j);
check1(i,j) = yes$(utc(i,j) =  0 and pc(i,j) <> 0);

*@ Helper Object: check2
*@ Description: supply links with nonzero cost but zero capacity
Set check2(i,j);
check2(i,j) = yes$(utc(i,j) <> 0 and pc(i,j) =  0);

display check1, check2;



*@ Function: supc
*@ Description: supply constant c
Parameter supc(i);
supc(i)  = sdat(i,"limit");
supc(i)$(supc(i) = inf) = 100;

*@ Function: supb
*@ Description: supply constant b
Parameter supb(i);
supb(i)  = ((sdat(i,"ref-p1") - sdat(i,"ref-p2"))
         / (1/(supc(i) - sdat(i,"ref-q1"))-1/(supc(i) - sdat(i,"ref-q2"))))
         $ (supc(i) <> inf);

*@ Function: supa
*@ Description: supply constant a
Parameter supa(i);
supa(i)  = sdat(i,"ref-p1") - supb(i)/(supc(i) - sdat(i,"ref-q1"));

* we rely on supa(i) evaluating to exactly zero in some cases
supa(i)          = round(supa(i),4);


sdat(i,"sup-a")  = supa(i);
sdat(i,"sup-b")  = supb(i);
display sdat;



*@ Function: demb
*@ Description: demand constant b
Parameter demb(j);
demb(j) = 1/ddat(j,"elas") + 1;

*@ Function: dema
*@ Description: demand constant a
Parameter dema(j);
dema(j) = ddat(j,"ref-p")/demb(j)/ddat(j,"ref-q")**(demb(j) - 1);

ddat(j,"dem-a") = dema(j);
ddat(j,"dem-b") = demb(j);
display ddat;



*@ Variable: x
*@ Description: shipment of natural gas (tcf)
Positive Variable  x(i,j);
x.up(i,j) = pc(i,j);

*@ Variable: s
*@ Description: regional supply (tcf)
Positive Variable s(i);
s.up(i)   = 0.99*supc(i);

*@ Variable: d
*@ Description: regional demand (tcf)
Positive Variable d(j);
d.lo(j)   = .2;
d.fx(jfx) = ddat(jfx,"ref-q");

*@ Variable: benefit
*@ Description: consumers benefits minus cost 
Variable benefit;


*@ Constraint: sb
*@ Description: supply balance (tcf) $$\sum_j x_{i,j} \leq s_i$$
Equation sb(i);
sb(i)..   sum(j$ij(i,j), x(i,j)) =l= s(i);

*@ Constraint: db
*@ Description: demand balance (tcf) $$\sum_i x_{i,j} \geq d_j$$
Equation db(j);
db(j)..   sum(i$ij(i,j), x(i,j)) =g= d(j);

*@ Constraint: bdef
*@ Description: benefit definition $$benefit=\sum_j dema_{j}d_j^{demb_{j}} - \sum_i (supa_{i}s_i - supb_{i} \log(\frac{supc_{i}-s_i}{supc_i}))-\sum_{i,j}utc_{i,j}x_{i,j}$$
Equation bdef;
bdef..    benefit =e= sum(j, dema(j)*d(j)**demb(j))
                   -  sum(i, supa(i)*s(i) - supb(i)*log((supc(i) - s(i))/supc(i)))
                   -  sum((i,j)$ij(i,j), utc(i,j)*x(i,j));

*@ Solver: solver
parameter solver(*);

*@ Problem: gtm
Model gtm 'gas transport model' / all /;

*option nlp = conopt;
solve gtm maximizing benefit using nlp;

solver('objective') = gtm.objVal;
solver('status') = gtm.solveStat;
solver('iterations') = gtm.iterUsd;
solver('time') = gtm.etSolver;



*@ Helper Object: report1
*@ Description: supply summary report
Parameter report1(i,*);
report1(i,"supply")   = s.l(i);
report1(i,"capacity") = s.up(i);
report1(i,"price")    = sb.m(i);


*@ Helper Object: report2
*@ Description: demand summary report
Parameter report2(j,*);
report2(j,"demand")   = d.l(j);
report2(j,"price")    = -db.m(j);

display report1, report2, x.l;

