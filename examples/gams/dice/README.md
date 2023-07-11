# DICE-99 Climate Policy Model
GAMS Code for DICE-99. Adapted from: `Nordhaus and Boyer, Warming the World (1999), Appendix E`.

# Overview
Utility ($U$) is maximized subject to constraints a sample of which is shown below. Utility increases as consumption ($C$) rises, which in turn is constrained by economic production ($Y$), which in turn is constrained by both abatements costs ($f$($\mu$)) and temperature increases ($T$).

$$\max U=\sum_t {r}_t L_t \log(\frac{C_t}{L_t})$$

$$C_t=Y_t-I_t$$

$$Y_t=tfp_t L_t^{1-\gamma} K_t^{\gamma} \frac{1-f(\mu_t)}{1+a_1{T}_t+a_2{T}_t^2}$$




# Inputs

* `stockdata`: csv file with stock information - number of stocks to choose from, and number of factors
* `L`: leverage limit
* `gamma`: risk aversion parameter


# Outputs

* `output.txt`: output file containing `w` vector, the allocation of stocks
* `allocation.png`: plot displaying allocation of stocks