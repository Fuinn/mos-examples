# mos-examples
Optimization model examples ready for use with [MOS](https://fuinn.ie/mos).

Examples are arranged by modeling system (e.g. CVXPY, JuMP). Associated with each example are two file types, ``*model.*`` and ``*api.*``, along with any data files associated with the example.

## Use with [MOS Frontend](https://mos.fuinn.ie)
The ``*model.*`` example may be uploaded to MOS Frontend directly, ready to be provided with mos-examples data or user data, and solved.


## Use with MOS Interface packages

Steps to use with the MOS [Python Interface package](https://github.com/Fuinn/mos-interface-py) or 
[Julia Interface package](https://github.com/Fuinn/mos-interface-jl):

* Installation of an MOS Interface package
* Adjustment of ``*api.*`` file to include URL and authentication token
* Alternatively, setting of local environment variables will allow use of the ``*api.*`` file directly
* The environment variables to set are:

The model may then be specified, adjusted, and solved through the ``*api.*`` file to the user's interests.