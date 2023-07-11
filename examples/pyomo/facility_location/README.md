# Facility Location

Model to choose $p$ facility locations from a set of candidates to meet geographically distributed customer demand.
Adapted from https://nbviewer.jupyter.org/github/Pyomo/PyomoGallery/blob/master/p_median/p_median.ipynb


# Overview

This formulation locates the $p$ facilities such that the demand weighted average distance is minimized between the facilities and the demand locations.


# Inputs

* `pmedian.dat`: input file where input parameters for number of facilities, $p$, number of candidate locations, $m$, and number of demand locations, $n$, are assigned.
* The demand weighted distance is randomly generated in this example.


# Outputs

* $x_{i,j}$: fraction of the demand of location $j$ supplied by facility $i$
* $y_{i}$: 1 if a facility is located at $i$, 0 otherwise