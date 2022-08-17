from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_simple_mip():

    # Interface
    interface = Interface()

    # Delte model
    interface.delete_model_with_name('Simple MIP JuMP Model')

    # New model
    model = interface.new_model('./examples/jump/simple_mip/simple_mip_model.jl')

    # Existing model by name
    model = interface.get_model_with_name('Simple MIP JuMP Model')

    # Set inputs
    model.set_input_object('lower_bound', 1,2)

    # Solve 
    model.run()

    assert(model.get_status() == 'success')

if __name__ == '__main__':
    test_simple_mip()

