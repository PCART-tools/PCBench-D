def C2F(C):
    """
    Convert Celsius to Fahrenheit

    Parameters
    ----------
    C : array_like
        Celsius temperature(s) to be converted.

    Returns
    -------
    F : float or array of floats
        Equivalent Fahrenheit temperature(s).

    Notes
    -----
    Computes ``F = 1.8 * C + 32``.

    Examples
    --------
    >>> from scipy.constants import C2F
    >>> C2F(np.array([-40, 40.0]))
    array([ -40.,  104.])

    """
    return 1.8 * _np.asanyarray(C) + 32
