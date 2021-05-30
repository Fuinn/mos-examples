import numpy as np 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delete model
interface.delete_model_with_name('Simple educational model')

# New model
model = interface.new_model('./examples/cvxpy/simple/simple_model.py')

# Get model by name
model = interface.get_model_with_name('Simple educational model')


assert(model.get_system() == 'cvxpy')
assert(model.get_status() == 'created')

# Run
model.run()

assert(model.get_status() == 'success')

print(model.get_execution_log())

