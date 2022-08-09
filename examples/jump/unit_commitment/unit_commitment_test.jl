using Pkg
Pkg.activate(".") 

import DotEnv
DotEnv.config()

using MOSInterface

# Interface
interface = Interface()

# Delete model
delete_model_with_name(interface, "Stochastic Unit Commitment")

# New model
model = new_model(interface, "./examples/jump/unit_commitment/unit_commitment_model.jl")

# Get model
model = get_model_with_name(interface, "Stochastic Unit Commitment")

# Set inputs
set_interface_object(model, "n_g", 10)
set_interface_object(model, "n_gsl", 5)

# Show info
println(get_name(model))
@assert(get_system(model) == "jump")
println(get_status(model))

# Solve
MOSInterface.run(model)
println(get_status(model))
