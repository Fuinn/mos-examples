import numpy as np
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delete model
interface.delete_model_with_name("Degenerate Codon Design")

# New model
model = interface.new_model('./examples/cvxpy/codon/decode.py')

# Get model by name
model = interface.get_model_with_name("Degenerate Codon Design")

# Set inputs
model.set_interface_object('MIP', True)

model.set_interface_file('D_file', './examples/cvxpy/codon/D.npy')

model.set_interface_file('D_hat_file', './examples/cvxpy/codon/D_hat.npy')

model.set_interface_file('s_file', './examples/cvxpy/codon/sequences.json')

# Run model
model.run()

print(model.get_status())
