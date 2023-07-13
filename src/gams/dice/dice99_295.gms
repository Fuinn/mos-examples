*@ Model:DICE99
*@ Description: GAMS Code for DICE-99. Adapted from: Nordhaus and Boyer, Warming the World, October 25 1999,   Appendix E. Utility is maximized subject to constraints a sample of which is shown below. Utility increases as consumption (C) rises, which in turn is constrained by economic production (Y), which in turn is constrained by both abatements costs (f(mu)) and temperature increases (T). $$\max UTILITY=\sum_t {RR}_t L_t \log(C_t / L_t)$$$$C_t=Y_t-I_t$$$$Y_t=AL_t^{1-\gamma} K_t^{\gamma} \frac{1-f(\mu_t)}{1+a_1{T}_t+a_2{T}_t^2}$$

*   MS&E 295 Homework 2, February 2017



*@ Helper Object: T
*@ Description: Time periods
Set    T          Time periods /1995,2000,2005,2010,2015,2020,2025,2030,2035,2040,2045,2050,2055,2060,2065,2070,2075,2080,2085,2090,2095,2100,2105,2110,2115,2120,2125,2130,2135,2140,2145,2150,2155,2160,2165,2170,2175,2180,2185,2190,2195,2200,2205,2210,2215,2220,2225,2230,2235,2240,2245,2250,2255,2260,2265,2270,2275,2280,2285,2290,2295,2300,2305,2310,2315,2320,2325,2330,2335/;


SETS
    TFIRST(T)  First period
    TLAST(T)   Last period
    tearly(T)  First 20 periods
    TLATE(T)   Second 20 periods;


TFIRST(T) = YES$(ORD(T) EQ 1);
TLAST(T)  = YES$(ORD(T) EQ CARD(T));
TEARLY(T) = YES$(ORD(T) LE 20);
TLATE(T)  = YES$(ORD(T) GE 21);


*@ Input Object: SRTP
*@ Description: Initial rate of social time preference (pct per year). Set at 3 in textbook.
Scalar SRTP     Initial rate of social time preference (pct per year) /3/     ;

*@ Input Object: fixedsavingrate
*@ Description: Fixed saving rate parameter (rate set as fraction), if set to zero, associated constraint not active
Scalar fixedsavingrate /0/;

*@ Input Object: carbonpolicy
*@ Description: Carbon policy switch, if set to zero, no control on emissions occurs. Any non-zero number turns on emissions controls
Scalar carbonpolicy /0/;



SCALARS
     A1       Damage coeff linear term                        /-.0045/
     A2       Damage coeff quadratic term                     /.0035/
     COST10   Intercept control cost function                 /.03/
     COST2    Exponent of control cost function               /2.15/
     dmiufunc Decline in cost of abatement function (pct per decade) /-8/
     decmiu   Change in decline of cost function (pct per year) /.5/
     DK       Depreciation rate on capital (pct per year)       /10/
     GAMA     Capital elasticity in production function       /.30/
     K0       1990 value capital trill 1990 US dollars        /47/
     LU0      Initial land use emissions (GtC per year)     /1.128/
     SIG0     CO2-equivalent emissions-GNP ratio              /.274/
     GSIGMA   Growth of sigma (pct per decade)                /-15.8854/
     desig    Decline rate of decarbonization (pct per decade) /2.358711/
     desig2   Quadratic term in decarbonization               /-.00085/
     WIEL     World industrial emissions limit (GtC per year) /5.67/
     LL0      1990 world population (millions)                /5632.7/
     GL0      Initial rowth rate of population (pct per decade) /15.7/
     DLAB     Decline rate of pop growth (pct per decade)       /22.2/
     A0       Initial level of total factor productivity      /.01685/
     GA0      Initial growth rate for technology (pct per decade) /3.8/
     DELA     Decline rate of technol. change per decade      /.000001/
     MAT1990  Concentration in atmosphere 1990 (b.t.c.)       /735/
     MU1990   Concentration in upper strata 1990 (b.t.c)      /781/
     ML1990   Concentration in lower strata 1990 (b.t.c)      /19230/
     b11      Carbon cycle transition matrix (pct per decade) /66.616/
     b12      Carbon cycle transition matrix                  /33.384/
     b21      Carbon cycle transition matrix                  /27.607/
     b22      Carbon cycle transition matrix                  /60.897/
     b23      Carbon cycle transition matrix                  /11.496/
     b32      Carbon cycle transition matrix                  /0.422/
     b33      Carbon cycle transition matrix                  /99.578/
     TL0      1985 lower strat. temp change (C) from 1900     /.06/
     T0       1985 atmospheric temp change (C)from 1900       /.43/
     C1       Climate-equation coefficient for upper level    /.226/
     CS       Eq temp increase for CO2 doubling (C)           /2.9078/
     C3       Transfer coeffic. upper to lower stratum        /.440/
     C4       Transfer coeffic for lower level                /.02/
     DR       Decline rate of social time preference (pct per year) /.25719/
     coefopt1     Scaling coefficient in the objective function  /333.51/
     coefopt2     Scaling coefficient in the objective function  /1493.76929/
;


*@ Function: gcost1
*@ Description: growth in abatement cost function
Parameter gcost1(t);
gcost1(T)=(dmiufunc/100)*EXP(-(decmiu/100)*10*(ORD(T)-1));

*@ Function: cost1
*@ Description: cost function for abatement
Parameter   cost1(t)         cost function for abatement;
cost1(TFIRST)=cost10;
LOOP(T,
cost1(T+1)=cost1(T)/((1+gcost1(T+1)));
);



*@ Function: ETREE
*@ Description: Emissions from deforestation
Parameter     ETREE(T)      Emissions from deforestation;
ETREE(T) = LU0*(1-0.1)**(ord(T)-1);

*@ Function: gsig
*@ Description: Cumulative improvement of energy efficiency
Parameter     GSIG(T)       Cumulative improvement of energy efficiency;
gsig(T)=(gsigma/100)*EXP (  -(desig/100)*10*(ORD(T)-1) - desig2*10* ((ord(t)-1)**2))   ;

*@ Function: SIGMA
*@ Description: CO2-equivalent-emissions output ratio
Parameter     SIGMA(T)      CO2-equivalent-emissions output ratio;
sigma(TFIRST)=sig0;
LOOP(T,
sigma(T+1)=(sigma(T)/((1-gsig(T+1))));
);


*@ Function: WEL
*@ Description:   World total emissions limit (GtC)
Parameter     WEL(T)        World total emissions limit (GtC);
WEL(T)=WIEL+ETREE(T);

*@ Function: GL
*@ Description: Growth rate of labor 0 to T
Parameter    GL(T)         Growth rate of labor 0 to T;
GL(T) = (GL0/DLAB)*(1-exp(-(DLAB/100)*(ord(t)-1)));


*@ Function: L
*@ Description: Level of population and labor
Parameter     L(T)          Level of population and labor;
L(T)=LL0*exp(GL(t));

*@ Function: GA
*@ Description: Growth rate of productivity from 0 to T
Parameter    GA(T)         Growth rate of productivity from 0 to T;
ga(T)=(ga0/100)*EXP(-(dela/100)*10*(ORD(T)-1));


*@ Function: AL
*@ Description: Level of total factor productivity
Parameter     AL(T)         Level of total factor productivity;
al(TFIRST) = a0;
LOOP(T,
al(T+1)=al(T)/((1-ga(T)));
);


*@ Function: FORCOTH
*@ Description: Exogenous forcing for other greenhouse gases
Parameter    FORCOTH(T)    Exogenous forcing for other greenhouse gases;
FORCOTH(T)=(-0.1965+(ORD(T)-1)*0.13465)$
         (ORD(T) LT 12) + 1.15$(ORD(T) GE 12);



*@ Function: R
*@ Description: Instantaeous rate of social time preference
Parameter    R(T)   Instantaeous rate of social time preference;
R(T)=(srtp/100)*EXP(-(DR/100)*10*(ORD(T)-1));

*@ Function: RR
*@ Description: Average utility social discount rate
Parameter  RR(T)    Average utility social discount rate;
RR(TFIRST)=1;
LOOP(T,
RR(T+1)=RR(T)/((1+R(T))**10);
);


**  Upper and Lower Bounds on variables are general conditions imposed for stability

*@ Variable: MIU
*@ Description: Emissions control rate GHGs
Positive Variable MIU(T) Emissions control rate GHGs;
MIU.up(T) = 100.0;
MIU.lo(T) = 0.000001;
* When miu is fixed to zero as above, there is no
* control on carbon, and no abatement occcurs. For our climate policy
* case, we want to allow controls to happen post 2015. So we constrain miu
* for the first two periods (1995 and 2005), and allow it to be
* unconstrained for future periods
MIU.fx(T)$(ORD(T) LE 2)= 0;

** Emissions control policy.
* If MIU is fixed (carbonpolicy=0), no control occurs
MIU.fx(t)$(not carbonpolicy)= 0;


*@ Variable: C
*@ Description: Consumption trill US dollars
Positive Variable    C(T)     Consumption trill US dollars;
C.lo(T)   = 2;

*@ Variable: Y
*@ Description: Output
Positive Variable    Y(T)     Output;

*@ Variable: I
*@ Description: Investment trill US dollars
Positive Variable    I(T)     Investment trill US dollars;

*@ Variable: K
*@ Description: Capital stock trill US dollars
Positive Variable     K(T)     Capital stock trill US dollars;
K.lo(T)   = 1;
K.FX(TFIRST) = K0;


*@ Variable: E
*@ Description: CO2-equivalent emissions bill t
Positive Variable     E(T)     CO2-equivalent emissions bill t;

*@ Variable: MAT
*@ Description: Carbon concentration in atmosphere (b.t.c.)
Positive Variable     MAT(T)   Carbon concentration in atmosphere (b.t.c.);
MAT.lo(T) = 10;
MAT.FX(TFIRST) = MAT1990;

*@ Variable: MU
*@ Description: Carbon concentration in shallow oceans (b.t.c.)
Positive Variable     MU(T)    Carbon concentration in shallow oceans (b.t.c.);
MU.lo(t)  = 100;
MU.FX(TFIRST) = MU1990;


*@ Variable: ML
*@ Description: Carbon concentration in lower oceans (b.t.c.)
Positive Variable    ML(T)    Carbon concentration in lower oceans (b.t.c.);
ML.lo(t)  = 1000;
ML.FX(TFIRST) = ML1990;


*@ Variable: TE
*@ Description: Temperature of atmosphere (C)
Positive Variable     TE(T)    Temperature of atmosphere (C);
TE.up(t)  = 12;
TE.FX(TFIRST) = T0;

*@ Variable: FORC
*@ Description: Temperature of atmosphere (C)
Variable     FORC(T)  Radiative forcing (W per m2 );

*@ Variable: TL
*@ Description: Temperature of lower ocean (C)
Variable    TL(T)    Temperature of lower ocean (C);
TL.FX(TFIRST) = TL0;

*@ Variable: UTILITY
*@ Description: Utility, item maximized
Variable    UTILITY;

*@ Constraint: UTIL
*@ Description: Objective function
Equation     UTIL      Objective function;
UTIL..          UTILITY =E= SUM(T, RR(T)*L(T)*LOG(C(T)/L(T))/coefopt1)+
		coefopt2 ;

*@ Constraint: YY
*@ Description: output equation
Equation  YY(T)     Output equation;
YY(T)..         Y(T) =E=
		AL(T)*L(T)**(1-GAMA)*K(T)**GAMA*(1-cost1(t)*((MIU(T)
		    /100)**cost2))/(1+a1*TE(T)+ a2*TE(T)**2);

*@ Constraint: CC
*@ Description: Consumption equation $$C_t=Y_t-I_t$$
Equation     CC(T)     Consumption equation;
CC(T)..         C(T) =E= Y(T)-I(T);

*@ Constraint: KK
*@ Description: Capital balance equation
Equation     KK(T)     Capital balance equation;
KK(T)..         K(T+1) =L= (1-(DK/100))**10 *K(T)+10*I(T);     

*@ Constraint: KC
*@ Description: Terminal condition for K 
Equation     KC(T)     ;
KC(TLAST)..     .02*K(TLAST) =L= I(TLAST);

*@ Constraint: EE
*@ Description: Emissions process
Equation     EE(T)     Emissions process;
EE(T)..
    E(T)=G=10*SIGMA(T)*(1-(MIU(T)/100))*AL(T)*L(T)**(1-GAMA)*K(T)**GAMA + ETREE(T);

*@ Constraint: FORCE
*@ Description: Radiative forcing equation
Equation      FORCE(T)  Radiative forcing equation;
FORCE(T)..      FORC(T) =E=  4.1*((log(Mat(T)/596.4)/log(2)))+FORCOTH(T);

*@ Constraint: TLE
*@ Description: Temperature-climate equation for lower oceans
Equation      TLE(T)    Temperature-climate equation for lower oceans;
TLE(T+1)..      TL(T+1) =E= TL(T)+C4*(TE(T)-TL(T));

*@ Constraint: TTE
*@ Description: Temperature-climate equation for atmosphere
Equation     TTE(T)    Temperature-climate equation for atmosphere;
TTE(T+1)..      TE(T+1) =E= TE(t)+C1*(FORC(t)-(4.1/CS)*TE(t)-C3*(TE(t)-TL(t)));

*@ Constraint: MMAT
*@ Description: Atmospheric concentration equation
Equation     MMAT(T)   Atmospheric concentration equation;
MMAT(T+1)..     MAT(T+1) =E= MAT(T)*(b11/100)+E(T)+MU(T)*(b21/100);


*@ Constraint: MMU
*@ Description: Shallow ocean concentration 
Equation     MMU(T)    Shallow ocean concentration;
MMU(T+1)..      MU(T+1) =E= MAT(T)*(b12/100)+MU(T)*(b22/100)+ML(T)*(b32/100);

*@ Constraint: MML
*@ Description: Lower ocean concentration 
Equation MML(T)    Lower ocean concentration;
MML(T+1)..      ML(T+1) =E= ML(T)*(b33/100)+(b23/100)*MU(T);


*@ Constraint: FSR
*@ Description: Constraint that fixes saving rate
Equation FSR       Constraint that fixes saving rate;
FSR(T)$fixedsavingrate..       I(T) =E= (AL(T)*L(T)**(1-GAMA)*K(T)**GAMA)*fixedsavingrate;




** ----------------------------
** ----------------------------

** Solution options

option iterlim = 99900;
option reslim = 99999;
option solprint = on;
option limrow = 0;
option limcol = 0;

*@ Problem: CO2
model CO2 /all/;

option nlp = conopt;

*@ Solver: solver
parameter solver(*);

solve CO2 maximizing UTILITY using nlp ;

** Display of results

display y.l, e.l, mat.l, te.l;

solver('objective') = CO2.objVal;
solver('status') = CO2.solveStat;
solver('iterations') = CO2.iterUsd;
solver('time') = CO2.etSolver;



*@ Helper Object: Indem
*@ Description: Industrial emissions (b.t.c. per year)
Parameter     Indem(t)   Industrial emissions (b.t.c. per year);
Indem(t) = e.l(t)-etree(t);

*@ Helper Object: Wem
*@ Description: Total emissions (b.t.c. per year)
Parameter     Wem(t)     Total emissions (b.t.c. per year);
Wem(t)   = e.l(t);

*@ Helper Object: S
*@ Description: Savings rate (pct) 
Parameter     S(t)       Savings rate (pct);
S(t) = 100*i.l(t)/y.l(t);

*@ Helper Object: consumption_per_capita
*@ Description: consumption per capital
Parameter    consumption_per_capita(t);
consumption_per_capita(t) = 1000*(C.L(t)/L(t));



display s;

Parameters
    Tax(t)    Carbon tax ($ per ton) - actually really environmental shadow price
    damtax(t) Concentration tax ($ per ton)
    dam(t)    Damages
    cost(t)   Abatement costs
    cprice(t) Price of carbon associated with emissions controls
;

tax(t)$(not tlast(t)) = -1*ee.m(t)*1000/(kk.m(t));
damtax(t)$(not tlast(t)) = -1*mmat.m(t)*1000/kk.m(t);
dam(t)    = y.l(t)*(1-1/(1+a1*te.l(t)+ a2*te.l(t)**2));
cost(t)   = y.l(t)*(cost1(t)*(miu.l(t)**cost2));

cprice(t) = (((miu.l(t)/100)**(cost2-1))*cost1(t)*cost2*1000)
            /
           (sigma(t)*(1+dam(t)/100));

*@ Output File: dice99_295.csv
File dice99_295/dice99_295.csv/;
dice99_295.pc=5;
dice99_295.pw=250;
Put dice99_295;
Put / "year";
Loop (tearly, put tearly.tl::0);
Put / "temp";
Loop (tearly, put te.l(tearly)::3);
Put / "conc";
Loop (tearly, put mat.l(tearly)::3);
Put / "discrate";
Loop (tearly, put rr(tearly)::5);
Put / "prod";
Loop (tearly, put al(tearly)::3);
Put / "exogforc";
Loop (tearly, put forcoth(tearly)::3);
Put / "pop";
Loop (tearly, put l(tearly)::3);
Put / "miu";
Loop (tearly, put miu.l(tearly)::3);
Put / "total emissions";
Loop (tearly, put wem(tearly)::3);
Put / "damages";
Loop (tearly, put dam(tearly)::5);
Put / "abatement cost";
Loop (tearly, put cost(tearly)::5);
Put / "Environmental shadow price";
Loop (tearly, put tax(tearly)::2);
Put / "Carbon price";
Loop (tearly, put cprice(tearly)::2);
Put / "savings rate";
Loop (tearly, put S(tearly)::2);
Put /"welfare";
Put utility.l::3;
Put /"consumption per capita";
Loop (tearly, put consumption_per_capita(tearly)::4);

