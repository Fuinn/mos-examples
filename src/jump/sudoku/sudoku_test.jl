import DotEnv
DotEnv.config()

using MOSInterface

@testset "Sudoku" begin

    # Interface
    interface = Interface()

    # Delete model
    delete_model_with_name(interface, "Sudoku JuMP Model")

    # New model
    model = new_model(interface, "./src/jump/sudoku/sudoku_model.jl")

    # Get model
    model = get_model_with_name(interface, "Sudoku JuMP Model")

    # Set inputs
    set_interface_file(model, "initial_grid_file", "./src/jump/sudoku/data.csv")

    # Show info
    @test get_name(model) == "Sudoku JuMP Model"
    @test get_system(model) == "jump"
    @test get_status(model) == "created"

    # Solve
    MOSInterface.run(model)

    # Status
    @test get_status(model) == "success"

end
