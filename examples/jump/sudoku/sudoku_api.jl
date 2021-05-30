using Pkg
Pkg.activate(".") 

import DotEnv
DotEnv.config()

using MOSInterface

# Interface
interface = Interface()

# Delete model
delete_model_with_name(interface, "Sudoku JuMP Model")

# New model
model = new_model(interface, "./examples/jump/sudoku/sudoku_model.jl")

# Get model
model = get_model_with_name(interface, "Sudoku JuMP Model")

# Set inputs
set_interface_file(model, "initial_grid_file", "./examples/jump/sudoku/data.csv")

# Show info
@assert(get_name(model) == "Sudoku JuMP Model")
@assert(get_system(model) == "jump")
@assert(get_status(model) == "created")

# Solve
MOSInterface.run(model)
@assert(get_status(model) == "success")