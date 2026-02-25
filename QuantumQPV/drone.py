import random
from measurement import measure_state


def legitimate_drone(state, basis_choice):
    """
    Honest drone measures in correct basis.
    """

    result = measure_state(state, basis_choice)

    processing_delay = 2e-6 + random.uniform(0, 1e-6)

    return result, basis_choice, processing_delay