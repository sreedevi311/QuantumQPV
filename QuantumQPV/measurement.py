import numpy as np
from qutip import basis, ket2dm, expect

def measure_state(state, basis_choice):

    if basis_choice == 0:   # Z basis
        proj0 = ket2dm(basis(2, 0))
        proj1 = ket2dm(basis(2, 1))
    else:                   # X basis
        plus = (basis(2, 0) + basis(2, 1)).unit()
        minus = (basis(2, 0) - basis(2, 1)).unit()
        proj0 = ket2dm(plus)
        proj1 = ket2dm(minus)

    p0 = expect(proj0, state)
    p1 = expect(proj1, state)

    return np.random.choice([0, 1], p=[p0, p1])