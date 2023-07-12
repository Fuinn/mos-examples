import DotEnv
DotEnv.config()

using MOSInterface

@testset "Unit Commitment" begin

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
    @test get_system(model) == "jump"

    # Solve
    MOSInterface.run(model)

    # Status
    @test get_status(model) == "success"

end