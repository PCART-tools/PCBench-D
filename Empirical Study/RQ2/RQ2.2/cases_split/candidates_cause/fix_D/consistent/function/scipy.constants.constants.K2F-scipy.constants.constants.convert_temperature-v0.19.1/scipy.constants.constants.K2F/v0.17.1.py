def K2F(K):
    """
    Convert Kelvin to Fahrenheit

    Parameters
    ----------
    K : array_like
        Kelvin temperature(s) to be converted.

    Returns
    -------
    F : float or array of floats
        Equivalent Fahrenheit temperature(s).

    Notes
    -----
    Computes ``F = 1.8 * (K - zero_Celsius) + 32`` where `zero_Celsius` =
    273.15, i.e., (the absolute value of) temperature "absolute zero" as
    measured in Celsius.

    Examples
    --------
    >>> from scipy.constants import K2F
    >>> K2F(np.array([233.15,  313.15]))
    array([ -40.,  104.])

    """
    return C2F(K2C(_np.asanyarray(K)))
