# mos-examples
Optimization model examples ready for use with [MOS](https://fuinn.ie/mos).

Examples are arranged by modeling system (e.g. CVXPY, JuMP). Associated with each example are two file types, ``*model.*`` and ``*api.*``, along with any data files associated with the example.

## Application areas

Examples from:
* Finance: [portfolio allocation](./examples/cvxpy/portfolio)
* Machine learning: [lasso regression](./examples/cvxpy/lasso)
* Logistics: [transportation](./examples/cvxpy/transportation), [facility location](./examples/pyomo/facility_location)
* Aerospace: [satellite scheduling](./examples/gams/satellite)
* Energy: [AC optimal power flow](./examples/optmod/acopf), [DC optimal power flow](./examples/optmod/dcopf), [gas trade](./examples/gams/gtm), [unit commitment](./examples/jump/unit_commitment)
* Climate policy: [Dice model](./examples/gams/dice)
* Macroeconomics: [computable general equilibrium](./examples/gams/mpsge)
* Resource allocation: [knapsack problem](./examples/jump/knapsack)
* Games: [sudoku](./examples/jump/sudoku)


## Use with [MOS Frontend](http://mos.fuinn.ie)
The ``*model.*`` example may be uploaded to MOS Frontend directly, ready to be provided with mos-examples data or user data, and solved.


## Use with MOS Interface packages

Steps to use with the MOS [Python Interface package](https://github.com/Fuinn/mos-interface-py) or 
[Julia Interface package](https://github.com/Fuinn/mos-interface-jl):

* Installation of an MOS Interface package
* Adjustment of an ``*api.*`` file to include URL and authentication token
* Alternatively, setting of local environment variables will allow use of an ``*api.*`` file directly
* The key environment variable to set is: ``MOS_BACKEND_TOKEN``. If hosting MOS locally, the environment variables ``MOS_BACKEND_HOST``, ``MOS_BACKEND_PORT``, are also required to be set.
* If the environment variables are set in a file named ``.env`` at the root of the repository, the api examples will automatically load them. 

The model may then be specified, adjusted, and solved through the ``*api.*`` file, from the repository root, to the user's interest.

<!-- CONTRIBUTING -->
## Contributing

Contributions of new and improved models are very welcome.

1. Fork the Project
2. Create your Branch (`git checkout -b NewModel`)
3. Commit your Changes (`git commit -m 'New Model'`)
4. Push to the Branch (`git push origin NewModel`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the BSD-3-Clause License. See `LICENSE` for more information.

