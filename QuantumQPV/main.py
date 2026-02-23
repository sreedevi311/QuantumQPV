from states import generate_random_state
from drone import legitimate_drone
from attack import intercept_resend_attack
from measurement import measure_state
from verifier import calculate_qber
from channel import apply_depolarizing_noise, photon_loss

ROUNDS = 200

def simulate(normal=True):
    sent_bits = []
    received_bits = []
    total_delay = 0
    detected_rounds = 0

    for _ in range(ROUNDS):

        # Step 1: Verifier prepares quantum state
        state, basis_choice, bit = generate_random_state()

        state = apply_depolarizing_noise(state)

        # Photon loss check
        if photon_loss():
            continue   # skip this round completely
        detected_rounds += 1

        # ---------------- NORMAL DRONE ----------------
        if normal:
            result, drone_basis, delay = legitimate_drone(state, basis_choice)

        # ---------------- SPOOFED CASE ----------------
        else:
            attacked_state, delay = intercept_resend_attack(state)

            # Drone claims correct basis measurement
            drone_basis = basis_choice
            result = measure_state(attacked_state, drone_basis)

        total_delay += delay

        # ---------------- BASIS SIFTING ----------------
        # Only compare bits when bases match
        if drone_basis == basis_choice:
            sent_bits.append(bit)
            received_bits.append(result)

    # Compute QBER
    qber = calculate_qber(sent_bits, received_bits)
    avg_delay = total_delay / ROUNDS
    detection_rate = detected_rounds / ROUNDS

    return qber, avg_delay, detection_rate

QBER_THRESHOLD = 0.15
DELAY_THRESHOLD = 0.005  # 5ms

def decision(qber, delay):
    if qber > QBER_THRESHOLD or delay > DELAY_THRESHOLD:
        return "⚠ SPOOF DETECTED"
    else:
        return "✅ LOCATION VERIFIED"

if __name__ == "__main__":

    qber_normal, delay_normal, det_normal = simulate(normal=True)
    qber_attack, delay_attack, det_attack = simulate(normal=False)

    print("\n--- NORMAL DRONE ---")
    print("QBER:", round(qber_normal, 3))
    print("Avg Delay:", round(delay_normal * 1000, 2), "ms")
    print(decision(qber_normal, delay_normal))
    print("Detection Rate:", round(det_normal, 3))

    print("\n--- SPOOFED DRONE ---")
    print("QBER:", round(qber_attack, 3))
    print("Avg Delay:", round(delay_attack * 1000, 2), "ms")
    print(decision(qber_attack, delay_attack))
    print("Detection Rate:", round(det_attack, 3))