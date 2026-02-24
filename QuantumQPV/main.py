from states import generate_random_state
from drone import legitimate_drone
from attack import intercept_resend_attack, replay_attack
from measurement import measure_state
from verifier import calculate_qber
from channel import apply_depolarizing_noise, photon_loss
from geometry import compute_distances, expected_time

ROUNDS = 200


def simulate(mode="normal"):

    sent_bits = []
    received_bits = []
    total_delay = 0
    detected_rounds = 0

    # ---- Geometry setup ----
    d1, d2 = compute_distances()        # true drone position
    t_expected = expected_time(d1, d2)  # expected relativistic time

    for _ in range(ROUNDS):

        # Step 1: Verifier prepares quantum state
        state, basis_choice, bit = generate_random_state()

        state = apply_depolarizing_noise(state)

        # Photon loss
        if photon_loss():
            continue

        detected_rounds += 1

        # ---------------- NORMAL DRONE ----------------
        if mode == "normal":

            result, drone_basis, processing_delay = legitimate_drone(
                state, basis_choice
            )

            delay = t_expected + processing_delay

        # ---------------- INTERCEPT ATTACK ----------------
        elif mode == "intercept":

            attacked_state, processing_delay = intercept_resend_attack(state)

            drone_basis = basis_choice
            result = measure_state(attacked_state, drone_basis)

            delay = t_expected + processing_delay

        # ---------------- REPLAY ATTACK ----------------
        elif mode == "replay":

            result, delay = replay_attack(state, basis_choice)
            drone_basis = basis_choice

        total_delay += delay

        # ---------------- BASIS SIFTING ----------------
        if drone_basis == basis_choice:
            sent_bits.append(bit)
            received_bits.append(result)

    # ---- Metrics ----
    qber = calculate_qber(sent_bits, received_bits)

    # IMPORTANT: average only over detected rounds
    if detected_rounds > 0:
        avg_delay = total_delay / detected_rounds
    else:
        avg_delay = 0

    detection_rate = detected_rounds / ROUNDS

    return qber, avg_delay, detection_rate, t_expected


# ---------------- Decision Engine ----------------

epsilon = 5e-5  # 50 microseconds tolerance
QBER_THRESHOLD = 0.15


def decision(qber, avg_delay, t_expected):

    geometry_valid = abs(avg_delay - t_expected) < epsilon

    if not geometry_valid:
        return "⚠ SPOOF DETECTED (Geometry mismatch)"

    if qber > QBER_THRESHOLD:
        return "⚠ SPOOF DETECTED (High QBER)"

    return "✅ LOCATION VERIFIED"


# ---------------- Main ----------------

if __name__ == "__main__":

    qber_normal, delay_normal, det_normal, t_expected = simulate(mode="normal")
    qber_intercept, delay_intercept, det_intercept, _ = simulate(mode="intercept")
    qber_replay, delay_replay, det_replay, _ = simulate(mode="replay")

    print("\n--- NORMAL DRONE ---")
    print("QBER:", round(qber_normal, 3))
    print("Avg Delay:", round(delay_normal, 6), "seconds")
    print(decision(qber_normal, delay_normal, t_expected))
    print("Detection Rate:", round(det_normal, 3))

    print("\n--- INTERCEPT ATTACK ---")
    print("QBER:", round(qber_intercept, 3))
    print("Avg Delay:", round(delay_intercept, 6), "seconds")
    print(decision(qber_intercept, delay_intercept, t_expected))
    print("Detection Rate:", round(det_intercept, 3))

    print("\n--- REPLAY ATTACK ---")
    print("QBER:", round(qber_replay, 3))
    print("Avg Delay:", round(delay_replay, 6), "seconds")
    print(decision(qber_replay, delay_replay, t_expected))
    print("Detection Rate:", round(det_replay, 3))