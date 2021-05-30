import numpy as np 
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delete model
interface.delete_model_with_name('Max flow')

# New model
model = interface.new_model('./examples/cvxpy/maxflow/maxflow_model.py')

# Get model by name
model = interface.get_model_with_name('Max flow')

assert(model.get_name() == 'Max flow')
assert(model.get_system() == 'cvxpy')
assert(model.get_status() == 'created')

# Run
model.run()

print('model status', model.get_status())
assert(len(model.get_execution_log()) > 0)

# Variable
x = model.get_variable_state('x', 'value')
assert(isinstance(x, np.ndarray))
print('x: ',x)

# Function
obj = model.get_function_state('objectivefn', 'value')
print('objective function',obj)

# Constraint
