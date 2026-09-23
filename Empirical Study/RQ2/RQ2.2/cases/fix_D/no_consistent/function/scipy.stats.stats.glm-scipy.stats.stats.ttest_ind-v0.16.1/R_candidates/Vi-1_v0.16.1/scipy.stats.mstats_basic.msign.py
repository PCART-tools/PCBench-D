def msign(x):
    """Returns the sign of x, or 0 if x is masked."""
    return ma.filled(np.sign(x), 0)
