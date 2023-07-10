# Stochastic Unit Commitment

Adapted from https://github.com/pajalevi/Stochastic_UC_model_julia.

# Overview

Find the dispatch schedule, $p$, for generators $g$, that minimizes costs across time $t$ and scenarios $o$

$$\min\sum_{g,t,o}(s_{g,t,o}+p_{g,t,o} varcost_g)$$

Subject to technical constraints, including:

$$\sum_g p_{g,t,o}={dem}_t\quad\forall t,o$$

$$s_{g,t,o}\geq v_{g,t,o}startup_g\quad\forall g,t,o$$

$$pmin_g u_{g,t,o} \leq p_{g,t,o} \leq pmax_g u_{g,t,o}\quad\forall g,t,o$$$$

$$v_{g,t+1,o}=u_{g,t+1,o}-u_{g,t,o}\quad\forall g,t,o$$$$

$$u,v\in(0,1),p,s\in\mathbb{R}$$




# Inputs

* `stockdata`: csv file with stock information - number of stocks to choose from, and number of factors
* `L`: leverage limit
* `gamma`: risk aversion parameter


# Outputs

* `output.txt`: output file containing `w` vector, the allocation of stocks
* `allocation.png`: plot displaying allocation of stocks