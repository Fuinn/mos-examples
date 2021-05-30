from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delte model
interface.delete_model_with_name('Stochastic Unit Commitment')

# New model
model = interface.new_model('./examples/jump/unit_commitment/unit_commitment_model.jl')

# Existing model by name
model = interface.get_model_with_name('Stochastic Unit Commitment')

# Set inputs
model.set_interface_object('n_g', 10)
model.set_interface_object('n_gsl', 5)


# Solve 
model.run()


print(model.get_execution_log())
print(model.get_status())
