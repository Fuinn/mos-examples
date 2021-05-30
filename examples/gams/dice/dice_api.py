from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delete model
interface.delete_model_with_name('DICE99')

# New model
model = interface.new_model('./examples/gams/dice/dice99_295.gms')

# Shot info
model.show_components()

# Set inputs
model.set_interface_object('SRTP', 3)
model.set_interface_object('fixedsavingrate', 0)
model.set_interface_object('carbonpolicy', 0)


# Solve
model.run()

# Status
print('\nstatus:')
print(model.get_status())

