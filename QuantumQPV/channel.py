from qutip import qeye
from config import NOISE_PROBABILITY, LOSS_PROBABILITY
import random

def apply_depolarizing_noise(state):

    p = NOISE_PROBABILITY
    I = qeye(2)
    rho = state.proj()

    noisy_rho = (1 - p) * rho + p * (I / 2)
    return noisy_rho


def photon_loss():

    # Returns True if photon is lost
    return random.random() < LOSS_PROBABILITY