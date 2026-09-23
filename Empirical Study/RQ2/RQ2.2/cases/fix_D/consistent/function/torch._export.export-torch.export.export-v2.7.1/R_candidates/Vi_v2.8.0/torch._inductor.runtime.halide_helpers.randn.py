def randn(seed, offset):
    i1, i2, _, _ = randint4x(seed, offset, PHILOX_N_ROUNDS_DEFAULT)
    u1 = _uint_to_uniform_float(i1)
    u2 = _uint_to_uniform_float(i2)
    n1, _ = _pair_uniform_to_normal(u1, u2)
    return n1
