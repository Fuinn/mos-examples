import numpy as np 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_portfolio():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Portfolio Model')

    # New model
    model = interface.new_model('./src/cvxpy/portfolio/portfolio_model.py')

    # Get model by name
    model = interface.get_model_with_name('Portfolio Model')

    # Set inputs
    model.set_interface_object('L', 2)
    model.set_interface_object('gamma', 0.1)
    model.set_interface_file('stockdata', './src/cvxpy/portfolio/stockdata.csv')

    assert(model.get_name() == 'Portfolio Model')
    assert(model.get_system() == 'cvxpy')
    assert(model.get_status() == 'created')

    # Run
    model.run()

    assert(model.get_status() == 'success')
    assert(len(model.get_execution_log()) > 0)

    # Variable
    w = model.get_variable_state('w', 'value')
    assert(isinstance(w, np.ndarray))
    assert(w.shape == (100,))

    # Function
    obj = model.get_function_state('objectivefn', 'value')
    assert(isinstance(obj, float))

    # Constraint
    alloc_vio = model.get_constraint_state('Allocation', 'violation')
    assert(isinstance(alloc_vio, float))
    assert(np.max(np.abs(alloc_vio)) < 1e-10)

if __name__ == '__main__':
    test_portfolio()
