# Computational General Equilibrium Example

Example 3 from https://www.gams.com/solvers/mpsge/gentle.htm

# Overview
This model investigates the labor-leisure decision. A single consumer is endowed with labor which is either supplied to the market or "repurchased" as leisure. The consumer utility function over market goods ($x$ and $y$) and leisure (L) is Cobb-Douglas:

$$U(x,y,L) = ln(x) + ln(y) + ln(L)$$

Goods $x$ and $y$ may only be purchased using funds obtained from labor sales. This constraint is written:

$$x + y = LPROD . LS$$

where goods $x$ and $y$ both have a price of unity at base year productivity, $LS$ is labor supply, and $LPROD$ is an index of labor productivity. An increase in productivity is equivalent to a proportional decrease in the prices of $x$ and $y$. 

Note in this version of MOS, that all prices and quantities from MPSGE are represented as variables.

