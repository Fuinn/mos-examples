from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_transportation():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Transportation Assignment')

    # New model
    model = interface.new_model('./src/cvxpy/transportation/transportation_model.py')

    # Get model by name
    model = interface.get_model_with_name('Transportation Assignment')
    assert(model.get_status() == 'created')

    # Set inputs
    model.set_interface_object('s', [500,700,800])
    model.set_interface_object('d', [400,900,200,500])
    model.set_interface_object('c', [[12,13,4,6],[6,4,10,11],[10,9,12,14]])

    model.run()

    assert(model.get_status() == 'success')

if __name__ == '__main__':
    test_transportation()

