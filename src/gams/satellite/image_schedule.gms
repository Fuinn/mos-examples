*@ Model: Satellite scheduling
*@ Description: James Merrick, Stanford University, code to find scheduling of image capture, based on discussion with Sreeja Nag PhD $$\max TOTAL$$$$TOTAL = \sum_{p,t} d_p O_{p,t}$$$$\sum_p O_{p,t} \leq 1 \quad \forall t$$$$O_{p,t} + \sum_{pp,tt \in lim_{p,t}}O_{pp,tt} \leq 1 \quad \forall p,t$$$$\sum_{{p,t}\in A_i} O_{p,t} \leq 1 \quad \forall i$$$$O\in\{0,1\}$$

* March 22nd 2017
* March 24th - reduce model size - key information is that sum((s,p,t),access(s,p,t,i))=1


sets
    s set of satellites
    ;

*@ Helper Object: p
*@ Description: pointing positions
Set    p pointing positions/p17*p19/;

*@ Helper Object: t
*@ Description: time (seconds)
Set     t time (seconds);


*@ Helper Object: i
*@ Description: set of images
Set    i set of images ;

*@ Helper Object: access
*@ Description: 1 if possible to capture image i from satellite s pointing in position p at time t
Set  access(s,p,t,i)  1 if possible to capture image i from satellite s pointing in position p at time t;


*@ Helper Object: a
*@ Description: set of pointing choices, p, at each time, t
Set a(p,t) access without the i;


alias(p,pp)
alias(t,tt)
set
    lim(p,t,pp,tt)  set of pp and tt associated with pt;


*@ Helper Object: d
*@ Description: distortion associated with each pointing p
Parameters  d(p)           distortion associated with each pointing p;

*@ Helper Object: dp
*@ Description: time to change from position p to position pp
Parameter dp(p,pp)       time to change from position p to position pp;


*@ Input File: data_in
$gdxin data_in.gdx
$load s,i,t
$load access, lim, d, dp
$gdxin

a(p,t)$sum((s,i),access(s,p,t,i)) = yes;


*@ Variable: O
*@ Description:       1 if an image is captured in pointing p at time t is captured, 0 otherwise
binary variable    O(p,t)          1 if image i is captured 0 otherwise    ;
O.fx(p,t)$(not a(p,t)) = 0;

*@ Variable: TOTAL
*@ Description: score maximized
variable    TOTAL    ;


*@ Constraint: Obj
*@ Description: Objective function, definition of total $$TOTAL=\sum_{p,t} O_{p,t} d_p$$
Equation     Obj     Objective function;
*note there is only one image associated with each s,p,tx
Obj..
    TOTAL =e= sum(a(p,t), O(p,t) * d(p));

*@ Constraint: Point
*@ Description: One pointing per time per satellite, each satellite can only point one direction at any time $$\sum_p O_{p,t}\leq 1 \quad \forall t$$
Equation     Point(t)   One pointing per time per satellite;
Point(t)..
    sum(p, O(p,t)) =l= 1;


*@ Constraint: Time
*@ Description: Constraint enforcing time required to shift pointing position, formulated as only one per set of combinations can be nonzero $$O_{p,t} + \sum_{pp,tt \in lim_{p,t}}O_{pp,tt} \leq 1 \quad \forall p,t$$
Equation    Time(p,t)    Time to shift position;
* attempt to model time it takes for satellite to change pointing direction
* most natural formulation seems to be a non-linear if-then structure
* this attempts to model it by saying if any O is one, then you have to wait dp before you can be one again
Time(p,t)$a(p,t)..
    O(p,t) + sum(lim(p,t,pp,tt), O(pp,tt)) =l= 1;


*@ Constraint: imagelim
*@ Description: Only one capture wanted of each image $$\sum_{{p,t}\in A_i} O_{p,t} \leq 1 \quad \forall i$$
Equation    imagelim(i)    ;
* We only want one capture of each image
imagelim(i)..
    sum(access(s,p,t,i), O(p,t)) =l= 1;



*@ Solver: solver
parameter solver(*);


*@ Problem: satellite
model satellite /all/;

solve satellite maximizing TOTAL using MIP;

solver('objective') = satellite.objVal;
solver('status') = satellite.solveStat;
solver('iterations') = satellite.iterUsd + 1;
solver('time') = satellite.etSolver;

display solver;

*@ Helper Object: image_capture
*@ Description: when captured
Parameter    image_capture(t,p);
image_capture(t,p) = O.L(p,t);


*@ Helper Object: image_capture_i
*@ Description: what images captured when
Parameter    image_capture_i(i,p,t);
* assign to image
image_capture_i(i,p,t)$sum(s,access(s,p,t,i)) = image_capture(t,p);

*@ Helper Object: number_captured
*@ Description: number of unique images captured
Parameter     number_captured    ;
number_captured("total") = sum((p,t), O.L(p,t));
