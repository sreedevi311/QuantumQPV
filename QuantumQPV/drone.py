import time
import random
from measurement import measure_state
import random

def legitimate_drone(state, basis_choice):

    result = measure_state(state, basis_choice)

    # Microsecond processing delay
    processing_delay = 2e-6 + random.uniform(0, 1e-6)

    return result, basis_choice, processing_delay