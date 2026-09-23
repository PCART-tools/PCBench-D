def randint(seed, offset, n_rounds=PHILOX_N_ROUNDS_DEFAULT):
    ret, _, _, _ = randint4x(seed, offset, n_rounds)
    return ret
