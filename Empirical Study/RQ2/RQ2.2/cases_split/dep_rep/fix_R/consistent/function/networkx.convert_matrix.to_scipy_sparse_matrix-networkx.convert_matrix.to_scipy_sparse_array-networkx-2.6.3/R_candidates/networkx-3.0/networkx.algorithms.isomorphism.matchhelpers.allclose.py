def allclose(x, y, rtol=1.0000000000000001e-05, atol=1e-08):
    """Returns True if x and y are sufficiently close, elementwise.

    Parameters
    ----------
    rtol : float
        The relative error tolerance.
    atol : float
        The absolute error tolerance.

    """
    # assume finite weights, see numpy.allclose() for reference
    for xi, yi in zip(x, y):
        if not math.isclose(xi, yi, rel_tol=rtol, abs_tol=atol):
            return False
    return True
