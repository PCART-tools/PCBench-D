def kei_zeros(nt):
    """Compute nt zeros of the Kelvin function kei(x).
    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("nt must be positive integer scalar.")
    return specfun.klvnzo(nt, 4)
