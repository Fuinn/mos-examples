import numpy as np 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface


def test_portfolio():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Constant Function Market Makers')

    # New model
    model = interface.new_model('./examples/cvxpy/constant_function_market_makers/arbitrage_model.py')

    # Get model by name
    model = interface.get_model_with_name('Constant Function Market Makers')

    assert(model.get_name() == 'Constant Function Market Makers')
    assert(model.get_system() == 'cvxpy')
    assert(model.get_status() == 'created')

    # Run
    model.run()

    assert(model.get_status() == 'success')
    assert(len(model.get_execution_log()) > 0)

    # Function
    obj = model.get_helper_object('output_value')
    assert(isinstance(obj, float))


if __name__ == '__main__':
    test_portfolio()
