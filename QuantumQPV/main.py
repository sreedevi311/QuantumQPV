from states import generate_random_state
from drone import legitimate_drone
from attack import intercept_resend_attack, replay_attack
from measurement import measure_state
from verifier import calculate_qber
from channel import apply_depolarizing_noise, photon_loss
from geometry import compute_distances, expected_time

import random

ROUNDS = 200


def simulate_live(noise_level, loss_prob, attack_strength, delay_offset):

    sent_bits = []
    received_bits = []
    total_delay = 0
    total_processing_delay = 0
    detected_rounds = 0

    d1, d2 = compute_distances()
    t_expected = expected_time(d1, d2)

    for _ in range(ROUNDS):

        state, basis_choice, bit = generate_random_state()

        # Apply channel noise
        state = apply_depolarizing_noise(state, noise_level)

        if photon_loss(loss_prob):
            continue

        detected_rounds += 1

        attack_roll = random.random()

        # ---------------- ATTACK ----------------
        if attack_roll < attack_strength:

            if random.random() < 0.5:
                # Intercept attack
                attacked_state, processing_delay = intercept_resend_attack(state)
                drone_basis = basis_choice
                result = measure_state(attacked_state, drone_basis)
                propagation_delay = t_expected

            else:
                # Replay attack
                result, propagation_delay, processing_delay = replay_attack(
                    state,
                    basis_choice,
                    delay_offset
                )
                drone_basis = basis_choice

        else:
            # Legitimate
            result, drone_basis, processing_delay = legitimate_drone(
                state,
                basis_choice
            )
            propagation_delay = t_expected

        total_processing_delay += processing_delay
        total_delay += propagation_delay + processing_delay

        if drone_basis == basis_choice:
            sent_bits.append(bit)
            received_bits.append(result)

    qber = calculate_qber(sent_bits, received_bits)

    if detected_rounds > 0:
        avg_delay = total_delay / detected_rounds
        avg_processing = total_processing_delay / detected_rounds
    else:
        avg_delay = 0
        avg_processing = 0

    # Expected total delay includes processing
    expected_total_delay = t_expected + avg_processing

    delay_deviation = abs(avg_delay - expected_total_delay)

    survival_rate = detected_rounds / ROUNDS

    return {
    "QBER": qber,
    "Avg_Delay": avg_delay,
    "Delay_Deviation": delay_deviation,
    "Detection_Rate": survival_rate,
    "Noise_Probability": noise_level,
    "Loss_Probability": loss_prob
}
    
import joblib
import pandas as pd
import time

if __name__ == "__main__":

    model = joblib.load("qpv_ml_model.pkl")

    label_map = {
        0: "SAFE",
        1: "INTERCEPT_ATTACK",
        2: "REPLAY_ATTACK"
    }

    while True:   # continuous loop

        results = simulate_live(
            noise_level=0.05,
            loss_prob=0.08,
            attack_strength=0.3,
            delay_offset=1e-6
        )

        test_input = pd.DataFrame([results])

        prediction = model.predict(test_input)[0]

        print("\nQuantum Features:")
        for k, v in results.items():
            print(f"{k}: {v}")

        print("ML Decision:", label_map.get(prediction))

        time.sleep(2)   # wait 2 seconds before next detection