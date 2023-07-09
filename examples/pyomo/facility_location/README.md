# Facility Location

Model to choose $p$ facility locations from a set of candidates to meet geographically distributed customer demand.
Adapted from https://nbviewer.jupyter.org/github/Pyomo/PyomoGallery/blob/master/p_median/p_median.ipynb


# Overview

This formulation locates the $p$ facilities such that the demand weighted average distance is minimized between the facilities and demand locations.

$$\min \sum_{i=1}^{n}\sum_{j=1}^{m}c_{ij}x_{ij}$$

$$\sum_{j=1}^m x_{ij}=s_i,\quad\forall i=1,2,\dots,m$$

$$\sum_{i=1}^n x_{ij}=d_j,\quad\forall j=1,2,\dots,n$$

$$x_{ij}\geq 0 \quad\forall i,j$$ 



# Inputs

* $s_i$: supply from each of $m$ warehouses
* $d_j$: demand from each of $n$ retailer locations
* $c_{ij}$: cost of transportation between supply $i$ and demand $j$


# Outputs

* $x_{ij}$: assignment between supply $i$ and demand $j$