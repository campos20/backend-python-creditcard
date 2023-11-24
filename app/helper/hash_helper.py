def hash_all_but_last_n_chars(sequence, n):
    return "X" * (len(sequence) - n) + sequence[-n:]
