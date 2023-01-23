from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_nurse_rostering():

    # Interface
    interface = Interface()

    # Delte model
    interface.delete_model_with_name('Nurse Rostering Model')

    # New model
    model = interface.new_model('./examples/jump/rostering/nurse_rostering_model.jl')

    # Existing model by name
    model = interface.get_model_with_name('Nurse Rostering Model')

    # Set inputs
    model.set_interface_object('max_off', 4)
    model.set_interface_file('nurses_shifts_unavailable', './examples/jump/rostering/out.csv')

    # Solve 
    model.run()

    assert(model.get_status() == 'success')

    print(model.get_execution_log())

if __name__ == '__main__':
    test_nurse_rostering()
