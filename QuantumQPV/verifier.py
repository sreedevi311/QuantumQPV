def calculate_qber(sent_bits, received_bits):
    errors = sum(s != r for s, r in zip(sent_bits, received_bits))
    return errors / len(sent_bits)