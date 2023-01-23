import DotEnv
DotEnv.config()

using MOSInterface

@testset "Nurse Rostering" begin

    # Interface
    interface = Interface()

    # Delete model
    delete_model_with_name(interface, "Nurse Rostering Model")

    # New model
    model = new_model(interface, "./examples/jump/rostering/nurse_rostering_model.jl")

    # Get model
    model = get_model_with_name(interface, "Nurse Rostering Model")

    # Set inputs
    set_interface_object(model, "max_off", 4)
    set_interface_file(model, "nurses_shifts_unavailable", "./examples/jump/rostering/out.csv")

    # Show info
    @test get_system(model) == "jump"

    # Solve
    MOSInterface.run(model)

    # Status
    @test get_status(model) == "success"

end
