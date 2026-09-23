def F2K(F):
    """
    Convert Fahrenheit to Kelvin

    Parameters
    ----------
    F : array_like
        Fahrenheit temperature(s) to be converted.

    Returns
    -------
    K : float or array of floats
        Equivalent Kelvin temperature(s).

    Notes
    -----
    Computes ``K = (F - 32)/1.8 + zero_Celsius`` where `zero_Celsius` =
    273.15, i.e., (the absolute value of) temperature "absolute zero" as
    measured in Celsius.

    Examples
    --------
    >>> from scipy.constants import F2K
    >>> F2K(np.array([-40, 104]))
    array([ 233.15,  313.15])

    """
    return C2K(F2C(_np.asanyarray(F)))
