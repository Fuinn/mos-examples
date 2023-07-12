import os
import numpy as np
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from mos.interface import Interface

def test_dcpf():

    # Interface
    interface = Interface()

    # Delete model
    interface.delete_model_with_name('DCOPF Model')

    # New model
    model = interface.new_model('./examples/optmod/dcopf/dcopf_model.py')

    # Existing model by name
    model = interface.get_model_with_name('DCOPF Model')

    # Set inputs
    model.set_interface_file('case', './examples/optmod/dcopf/ieee14.m')
    model.set_interface_object('feastol', 1.5e-3)

    assert(model.get_name() == 'DCOPF Model')
    assert(model.get_system() == 'optmod')
    assert(model.get_status() == 'created')

    # Initial types and shapes
    t, s = model.get_variable_type_and_shape('P')
    assert(t == 'unknown')
    assert(s is None)

    # Run
    model.run()

    # Status
    assert(model.get_status() == 'success')

    # Input file
    f = model.get_interface_file('case')
    ff = open(f, 'r')
    ff.close()
    os.remove(f)

    # Input object
    assert(model.get_interface_object('feastol') == 1.5e-3)

    # Helper object
    assert(model.get_helper_object('net')['base_power'] == 100)

    # Variable 
    t, s = model.get_variable_type_and_shape('P')
    assert(t == 'hashmap')
    assert(isinstance(s, tuple))
    assert(s == (5,))
    P = model.get_variable_state('P', 'value')
    assert(isinstance(P, dict))
    assert(len(P) == 5)
    for i in range(5):
        assert(i in P)

    # Function
    gen_cost = model.get_function_state('gen_cost', 'value')
    assert(isinstance(gen_cost, float))
    assert(abs(gen_cost-7642) < 1)

    # Constraint
    pcb_vio = model.get_constraint_state('power_balance', 'violation')
    assert(isinstance(pcb_vio, np.ndarray))
    assert(pcb_vio.shape == (14,))
    assert(pcb_vio.dtype == float)
    assert(np.max(np.abs(pcb_vio)) < 1e-10)

    # Solver state
    s = model.get_solver_state()
    assert(isinstance(s, dict))
    assert(s['status'] == 'solved')

    # Problem state
    s = model.get_problem_state()
    assert(isinstance(s, dict))

    # Output file
    f = model.get_interface_file('output')
    ff = open(f, 'r')
    ff.close()
    os.remove(f)

    # Output object
    o = model.get_interface_object('output_obj')
    assert(isinstance(o, list))
    assert(len(o) == 4)

    # Execution log
    assert(isinstance(model.get_execution_log(), str))
    assert(len(model.get_execution_log()) > 0)

if __name__ == '__main__':
    test_dcpf()
