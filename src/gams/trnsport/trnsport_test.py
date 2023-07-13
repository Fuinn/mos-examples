from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_trnsport():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('Transportation Model')

    # New model
    model = interface.new_model('./src/gams/trnsport/trnsport.gms')

    # Shot info
    model.show_components()

    # Set inputs
    model.set_interface_object('f', 90)
    model.set_interface_file('d', './src/gams/trnsport/d.inc')

    # Solve
    model.run()

    # Status
    assert(model.get_status() == 'success')

if __name__ == '__main__':
    test_trnsport()

