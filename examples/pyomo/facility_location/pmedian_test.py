from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_facility_location():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Facility Location')

    # New model
    model = interface.new_model('./examples/pyomo/facility_location/pmedian+model.py')

    # Get model by name
    model = interface.get_model_with_name('Facility Location')

    # Set inputs
    model.set_interface_file('data', './examples/pyomo/facility_location/pmedian.dat')

    assert(model.get_system() == 'pyomo')
    assert(model.get_status() == 'created')

    # Run
    model.run()

    assert(model.get_status() == 'success')
    assert(len(model.get_execution_log()) > 0)
    print(model.get_execution_log())

    # Function
    obj = model.get_function_state('cost', 'value')

    print('objective value: ', obj)

    assert(isinstance(obj, float))

    # Constraint
    pass

if __name__ == '__main__':
    test_facility_location()