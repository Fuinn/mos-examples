# Satellite image capture scheduling

Model to schedule earth image capture by orbiting satellites. Associated paper is Nag et al. (2018) https://www.sciencedirect.com/science/article/abs/pii/S0273117717308050

# Overview

This formulation locates the $p$ facilities such that the demand weighted average distance is minimized between the facilities and the demand locations.


# Inputs

* `pmedian.dat`: input file where input parameters for number of facilities, $p$, number of candidate locations, $m$, and number of demand locations, $n$, are assigned.
* The demand weighted distance is randomly generated in this example.


# Outputs

* $x_{i,j}$: fraction of the demand of location $j$ supplied by facility $i$
* $y_{i}$: 1 if a facility is located at $i$, 0 otherwise