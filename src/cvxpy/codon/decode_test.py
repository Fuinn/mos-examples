import numpy as np
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_codon():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name("Degenerate Codon Design")

    # New model
    model = interface.new_model('./src/cvxpy/codon/decode_model.py')

    # Get model by name
    model = interface.get_model_with_name("Degenerate Codon Design")

    # Set inputs
    model.set_interface_object('MIP', False)

    model.set_interface_file('D_file', './src/cvxpy/codon/D.npy')

    model.set_interface_file('D_hat_file', './src/cvxpy/codon/D_hat.npy')

    model.set_interface_file('s_file', './src/cvxpy/codon/sequences.json')

    # Run model
    model.run()

    assert(model.get_status() == 'success')

if __name__ == '__main__':
    test_codon()
