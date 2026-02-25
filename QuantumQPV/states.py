from qutip import basis, ket2dm
import random

zero = ket2dm(basis(2, 0))
one = ket2dm(basis(2, 1))

plus = ket2dm((basis(2, 0) + basis(2, 1)).unit())
minus = ket2dm((basis(2, 0) - basis(2, 1)).unit())


def generate_random_state():
    basis_choice = random.choice([0, 1])   # 0=Z, 1=X
    bit = random.choice([0, 1])

    if basis_choice == 0:
        state = zero if bit == 0 else one
    else:
        state = plus if bit == 0 else minus

    return state, basis_choice, bit