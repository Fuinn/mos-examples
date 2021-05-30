from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

# Interface
interface = Interface()

# Delete model
interface.delete_model_with_name('A Transportation Problem')

# New model
model = interface.new_model('./examples/gams/trnsport/trnsport.gms')

# Shot info
model.show_components()

# Set inputs
model.set_interface_object('f', 90)
model.set_interface_file('d', './examples/gams/trnsport/d.inc')

# Solve
model.run()

# Status
print('\nstatus:')
print(model.get_status())

