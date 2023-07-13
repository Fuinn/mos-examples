import DotEnv
DotEnv.config()

using MOSInterface

@testset "Simple_MIP" begin
    # Interface
    interface = Interface()

    # Delete model
    delete_model_with_name(interface, "Simple MIP JuMP Model")

    # New model
    model = new_model(interface, "./src/jump/simple_mip/simple_mip_model.jl")

    # Get model
    model = get_model_with_name(interface, "Simple MIP JuMP Model")

    # Set inputs
    set_interface_object(model, "lower_bound", 1.2)

    # Show info
    @test get_name(model) == "Simple MIP JuMP Model"
    @test get_system(model) == "jump"
    @test get_status(model) == "created"

    # Solve
    MOSInterface.run(model)

    # Status
    @test get_status(model) == "success"

end    
