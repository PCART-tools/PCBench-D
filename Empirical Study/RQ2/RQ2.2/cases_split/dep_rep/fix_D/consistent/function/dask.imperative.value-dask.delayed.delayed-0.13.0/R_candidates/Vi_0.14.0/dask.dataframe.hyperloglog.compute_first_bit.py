def compute_first_bit(a):
    "Compute the position of the first nonzero bit for each int in an array."
    # TODO: consider making this less memory-hungry
    bits = np.bitwise_and.outer(a, 1 << np.arange(32))
    bits = bits.cumsum(axis=1).astype(np.bool)
    return 33 - bits.sum(axis=1)
