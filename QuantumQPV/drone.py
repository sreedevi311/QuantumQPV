import time
import random
from measurement import measure_state

def legitimate_drone(state, basis_choice):
    drone_basis = basis_choice  # exact same basis
    result = measure_state(state, drone_basis)
    delay = 0.002 + random.uniform(0, 0.001)
    return result, drone_basis, delay