SPEED_OF_LIGHT = 3e8  # m/s

from config import V1_POSITION, V2_POSITION, DRONE_POSITION

def compute_distances(position=None):

    if position is None:
        position = DRONE_POSITION

    d1 = abs(position - V1_POSITION)
    d2 = abs(V2_POSITION - position)
    return d1, d2


def expected_time(d1, d2):
    return (d1 + d2) / SPEED_OF_LIGHT