from qutip import basis
import random

zero = basis(2, 0)
one = basis(2, 1)

plus = (zero + one).unit()
minus = (zero - one).unit()

def generate_random_state():
    basis_choice = random.choice([0, 1])   # 0=Z, 1=X
    bit = random.choice([0, 1])

    if basis_choice == 0:   # Z
        state = zero if bit == 0 else one
    else:                   # X
        state = plus if bit == 0 else minus

    return state, basis_choice, bit