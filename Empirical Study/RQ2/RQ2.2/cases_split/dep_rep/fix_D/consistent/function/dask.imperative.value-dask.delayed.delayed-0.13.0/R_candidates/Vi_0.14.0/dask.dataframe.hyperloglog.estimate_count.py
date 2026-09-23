def estimate_count(Ms, b):
    m = 1 << b

    # Combine one last time
    M = reduce_state(Ms, b)

    # Estimate cardinality, no adjustments
    alpha = 0.7213 / (1 + 1.079 / m)
    E = alpha * m / (2.0 ** -M.astype('f8')).sum() * m
    #                        ^^^^ starts as unsigned, need a signed type for
    #                             negation operator to do something useful

    # Apply adjustments for small / big cardinalities, if applicable
    if E < 2.5 * m:
        V = (M == 0).sum()
        if V:
            return m * np.log(m / V)
    if E > 2**32 / 30.0:
        return -2**32 * np.log1p(-E / 2**32)
    return E
