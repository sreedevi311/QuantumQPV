import random
import time
from turtle import delay
from measurement import measure_state
from states import zero, one, plus, minus

def intercept_resend_attack(state):
    guessed_basis = random.choice(["Z", "X"])
    measured_bit = measure_state(state, guessed_basis)

    if guessed_basis == "Z":
        new_state = zero if measured_bit == 0 else one
    else:
        new_state = plus if measured_bit == 0 else minus

    processing_delay = 2e-6 + random.uniform(0, 1e-6)
    time.sleep(processing_delay)

    return new_state, processing_delay

import random
from measurement import measure_state
from geometry import compute_distances, expected_time

FAKE_POSITION = 220_000  # attacker not at 150km center


def replay_attack(state, basis_choice):

    # Attacker measures in correct basis (no disturbance)
    measured_bit = measure_state(state, basis_choice)

    # Geometry from WRONG position
    d1_fake, d2_fake = compute_distances(position=FAKE_POSITION)
    t_fake = expected_time(d1_fake, d2_fake)

    # Microsecond processing delay
    processing_delay = 2e-6 + random.uniform(0, 1e-6)

    total_delay = t_fake + processing_delay

    return measured_bit, total_delay