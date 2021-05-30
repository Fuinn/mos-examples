import os
import numpy as np
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delete model
interface.delete_model_with_name('ACOPF Model')

# New model
model = interface.new_model('./examples/optmod/acopf/acopf_model.py')

# Existing model by name
model = interface.get_model_with_name('ACOPF Model')

# Set inputs
model.set_interface_file('case', './examples/optmod/acopf/ieee14.m')
model.set_interface_object('feastol', 1.5e-3)

assert(model.get_name() == 'ACOPF Model')
assert(model.get_system() == 'optmod')
assert(model.get_status() == 'created')

# Initial types and shapes
t, s = model.get_variable_type_and_shape('P')
print(t,s)

# Run
model.run()

# Status
print(model.get_status())
assert(model.get_status() == 'success')

