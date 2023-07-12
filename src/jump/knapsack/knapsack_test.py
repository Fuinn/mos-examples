from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_knapsack():

    # Interface
    interface = Interface()

    # Delte model
    interface.delete_model_with_name('Knapsack Model')

    # New model
    model = interface.new_model('./examples/jump/knapsack/knapsack_model.jl')

    # Existing model by name
    model = interface.get_model_with_name('Knapsack Model')

    # Set inputs
    model.set_interface_file('profit_file', 
                    './examples/jump/knapsack/profit.json')
    model.set_interface_object('weight',
                    [2, 8, 4, 2, 5])
    model.set_interface_object('capacity',
                        10)

    # Solve 
    model.run()

    assert(model.get_status() == 'success')

    print('')
    print('EXECUTION LOG')
    print('*************')
    print(model.get_execution_log())

if __name__ == '__main__':
    test_knapsack()

