from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_sudoku():

    # Interface
    interface = Interface()

    # Delte model
    interface.delete_model_with_name('Sudoku JuMP Model')

    # New model
    model = interface.new_model('./src/jump/sudoku/sudoku_model.jl')

    # Existing model by name
    model = interface.get_model_with_name('Sudoku JuMP Model')

    # Set inputs
    model.set_interface_file('initial_grid_file', './src/jump/sudoku/data.csv')

    # Solve 
    model.run()

    assert(model.get_status() == 'success')

if __name__ == '__main__':
    test_sudoku()

