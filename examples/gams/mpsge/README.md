# Computational General Equilibrium Example

MPSGE Example 3 from https://www.gams.com/solvers/mpsge/gentle.htm Note in this version of MOS, that all prices and quantities from MPSGE come through as variables.$$$$This model investigates the labor-leisure decision. A single consumer is endowed with labor which is either supplied to the market or "repurchased" as leisure. The consumer utility function over market goods (x and y) and leisure is Cobb-Douglas:$$U(x,y,L) = ln(x) + ln(y) + ln(L)$$ Goods x and y may only be purchased using funds obtained from labor sales. This constraint is written:$$x + y = LPROD . LS$$ where goods x and y both have a price of unity at base year productivity and LPROD is an index of labor productivity. An increase in productivity is equivalent to a proportional decrease in the prices of x and y. 


# Overview
Utility ($U$) is maximized subject to constraints a sample of which is shown below. Utility increases as consumption ($C$) rises, which in turn is constrained by economic production ($Y$), which in turn is constrained by both abatements costs ($f$($\mu$)) and temperature increases ($T$).

$$\max U=\sum_t {r}_t L_t \log(\frac{C_t}{L_t})$$

$$C_t=Y_t-I_t$$

$$Y_t=\alpha_t L_t^{1-\gamma} K_t^{\gamma} \frac{1-f(\mu_t)}{1+a_1{T}_t+a_2{T}_t^2}$$


Where $L_t$ and $I_t$ are model variables representing labour and investment respectively. While $r_t$ and $\alpha_t$ are input parameters representing the discount rate and total factor productivity respectively.