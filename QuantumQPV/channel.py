import random
from qutip import qeye


def apply_depolarizing_noise(state, noise_level):
    """
    Applies depolarizing noise to a density matrix.
    """

    I = qeye(2)

    # state is already a density matrix
    noisy_rho = (1 - noise_level) * state + noise_level * (I / 2)

    return noisy_rho


def photon_loss(loss_probability):
    return random.random() < loss_probability