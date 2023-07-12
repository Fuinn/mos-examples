import numpy as np 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_lasso():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Lasso')

    # New model
    model = interface.new_model('./examples/cvxpy/lasso/lasso_model.py')

    # Get model by name
    model = interface.get_model_with_name('Lasso')

    # Set inputs
    model.set_interface_object('lambd', 0.1)

    assert(model.get_name() == 'Lasso')
    assert(model.get_system() == 'cvxpy')
    assert(model.get_status() == 'created')

    # Run
    model.run()

    assert(model.get_status() == 'success')
    assert(len(model.get_execution_log()) > 0)

    # Variable
    beta = model.get_variable_state('beta', 'value')
    assert(isinstance(beta, np.ndarray))
    print('coeffficients of beta are: ',beta)

    # Function
    obj = model.get_function_state('objectivefn', 'value')
    assert(isinstance(obj, float))

    # Constraint
    pass

if __name__ == '__main__':
    test_lasso()

