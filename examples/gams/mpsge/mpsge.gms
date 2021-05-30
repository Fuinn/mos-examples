*@ Model: MPSGE
*@ Description: MPSGE Example 3 from https://www.gams.com/solvers/mpsge/gentle.htm Note in this version of MOS, that all prices and quantities from MPSGE come through as variables.$$$$This model investigates the labor-leisure decision. A single consumer is endowed with labor which is either supplied to the market or "repurchased" as leisure. The consumer utility function over market goods (x and y) and leisure is Cobb-Douglas:$$U(x,y,L) = ln(x) + ln(y) + ln(L)$$ Goods x and y may only be purchased using funds obtained from labor sales. This constraint is written:$$x + y = LPROD . LS$$ where goods x and y both have a price of unity at base year productivity and LPROD is an index of labor productivity. An increase in productivity is equivalent to a proportional decrease in the prices of x and y. 

*@ Input object: LPROD
*@ Description: Index of aggregate labor productivity (set at 1 in example)
Scalar LPROD   AGGREGATE LABOR PRODUCTIVITY /1/;

*@ Helper object: CX
*@ Description: Cost of X at base year productivity
Scalar          CX      COST OF X AT BASE YEAR PRODUCTIVITY /1/;

*@ Helper object: CY
*@ Description: Cost of Y at base year productivity
Scalar          CY      COST OF Y AT BASE YEAR PRODUCTIVITY /1/;


$ONTEXT

*@ Problem: LSUPPLY
$MODEL:LSUPPLY

$SECTORS:
*@ Variable: X
*@ Description: Clearing Market Quantity for Good X    
        X       ! SUPPLY=DEMAND FOR X
*@ Variable: Y
*@ Description: Clearing Market Quantity for Good Y
        Y       ! SUPPLY=DEMAND FOR Y
*@ Variable: LS
*@ Description: Labor Supply	
        LS      ! LABOR SUPPLY

$COMMODITIES:
*@ Variable: PX
*@ Description: Market price of good X
        PX      ! MARKET PRICE OF GOOD X
*@ Variable: PY
*@ Description: Market price of good Y
        PY      ! MARKET PRICE OF GOOD Y
*@ Variable: PL
*@ Description: Market wage
        PL      ! MARKET WAGE
*@ Variable: PLS
*@ Description: Consumer value of leisure
        PLS     ! CONSUMER VALUE OF LEISURE

$CONSUMERS:
*@ Variable: RA
*@ Description: Representative Agent
        RA      ! REPRESENTATIVE AGENT

$PROD:LS
        O:PL    Q:LPROD
        I:PLS   Q:1

$PROD:X
        O:PX    Q:1
        I:PL    Q:CX

$PROD:Y
        O:PY    Q:1
        I:PL    Q:CY

$DEMAND:RA  s:1
        E:PLS   Q:120
        D:PLS   Q:1     P:1
        D:PX    Q:1     P:1
        D:PY    Q:1     P:1

$OFFTEXT
$SYSINCLUDE mpsgeset LSUPPLY

$INCLUDE LSUPPLY.GEN
SOLVE LSUPPLY USING MCP;

*@ Solver: solver
parameter solver(*);
solver('objective') = LSUPPLY.objVal;
solver('status') = LSUPPLY.solveStat;
solver('iterations') = LSUPPLY.iterUsd;
solver('time') = LSUPPLY.etSolver;

