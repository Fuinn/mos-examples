import DotEnv
DotEnv.config()

using MOSInterface

@testset "Portfolio" begin

    # Interface
    interface = Interface()

    # Delete model
    delete_model_with_name(interface, "Portfolio Model")

    # New model
    model = new_model(interface, "./examples/cvxpy/portfolio/portfolio_model.py")

    # Get model
    model = get_model_with_name(interface, "Portfolio Model")

    # Set inputs
    set_interface_object(model, "L", 2)
    set_interface_object(model, "gamma", 0.1)
    set_interface_file(model, "stockdata", "examples/cvxpy/portfolio/stockdata.csv")

    @test get_name(model) == "Portfolio Model"
    @test get_system(model) == "cvxpy"
    @test get_status(model) == "created"

    # Solve
    MOSInterface.run(model)

    @test get_status(model) == "success"

end