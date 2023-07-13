import numpy as np 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_simple():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Simple educational model')

    # New model
    model = interface.new_model('./src/cvxpy/simple/simple_model.py')

    # Get model by name
    model = interface.get_model_with_name('Simple educational model')

    assert(model.get_system() == 'cvxpy')
    assert(model.get_status() == 'created')

    # Run
    model.run()

    assert(model.get_status() == 'success')

    print(model.get_execution_log())

if __name__ == '__main__':
    test_simple()

