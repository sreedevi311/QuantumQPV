import random
import time
from measurement import measure_state
from states import zero, one, plus, minus

def intercept_resend_attack(state):
    guessed_basis = random.choice(["Z", "X"])
    measured_bit = measure_state(state, guessed_basis)

    if guessed_basis == "Z":
        new_state = zero if measured_bit == 0 else one
    else:
        new_state = plus if measured_bit == 0 else minus

    delay = 0.01 + random.uniform(0, 0.005)  # 10ms+
    time.sleep(delay)

    return new_state, delay