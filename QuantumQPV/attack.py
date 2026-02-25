import random
from measurement import measure_state
from states import zero, one, plus, minus
from geometry import compute_distances, expected_time


FAKE_POSITION = 220_000  # attacker spoofed location


def intercept_resend_attack(state):
    """
    Eve randomly guesses basis and resends measured state.
    Causes QBER increase.
    """

    guessed_basis = random.choice([0, 1])
    measured_bit = measure_state(state, guessed_basis)

    if guessed_basis == 0:
        new_state = zero if measured_bit == 0 else one
    else:
        new_state = plus if measured_bit == 0 else minus

    processing_delay = 2e-6 + random.uniform(0, 1e-6)

    return new_state, processing_delay


def replay_attack(state, basis_choice, delay_offset):
    """
    Attacker measures correctly but responds from wrong geometry.
    Causes timing deviation.
    """

    measured_bit = measure_state(state, basis_choice)

    d1_fake, d2_fake = compute_distances(position=FAKE_POSITION)
    t_fake = expected_time(d1_fake, d2_fake)

    processing_delay = 2e-6 + random.uniform(0, 1e-6)

    # Return propagation delay separately
    propagation_delay = t_fake + delay_offset

    return measured_bit, propagation_delay, processing_delay