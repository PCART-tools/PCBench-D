def rand(seed, offset, n_rounds=PHILOX_N_ROUNDS_DEFAULT):
    source = randint(seed, offset, n_rounds)
    return _uint_to_uniform_float(source)
