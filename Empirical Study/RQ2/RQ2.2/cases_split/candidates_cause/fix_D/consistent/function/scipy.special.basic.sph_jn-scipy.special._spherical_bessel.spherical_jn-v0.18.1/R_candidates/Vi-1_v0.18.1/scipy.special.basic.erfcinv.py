def erfcinv(y):
    """Inverse function for erfc.
    """
    return -ndtri(0.5*y)/sqrt(2)
