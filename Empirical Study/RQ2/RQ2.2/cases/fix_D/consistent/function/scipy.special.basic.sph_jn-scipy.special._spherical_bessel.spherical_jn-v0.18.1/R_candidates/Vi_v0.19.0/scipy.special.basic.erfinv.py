def erfinv(y):
    """Inverse function for erf.
    """
    return ndtri((y+1)/2.0)/sqrt(2)
