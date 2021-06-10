# mos-examples
Optimization model examples ready for use with [MOS](https://fuinn.ie/mos).

Examples are arranged by modeling system (e.g. CVXPY, JuMP). Associated with each example are two files, ``*model.py`` and ``*api.py``, along with any data files associated with the example.

## Use with [MOS Frontend](https://mos.fuinn.ie)
The ``*model.py`` example may be uploaded to MOS Frontend directly, ready to be provided with mos-examples or user data, and solved.


## Use with MOS Interface packages

Steps to use with the MOS [Python Interface package](https://github.com/Fuinn/mos-interface-py) or 
[Julia Interface package](https://github.com/Fuinn/mos-interface-jl):

* Adjustment of ``*api.py`` file to include URL and authentication token
* Alternatively setting of local environment variables will allow use of the ``*api.py`` file directly

The model may be specified, adjusted, and solved through the ``*api.py`` file to the user's interests.