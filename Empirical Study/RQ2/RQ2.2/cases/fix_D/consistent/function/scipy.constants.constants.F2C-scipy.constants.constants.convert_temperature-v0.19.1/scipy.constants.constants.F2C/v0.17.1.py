def F2C(F):
    """
    Convert Fahrenheit to Celsius

    Parameters
    ----------
    F : array_like
        Fahrenheit temperature(s) to be converted.

    Returns
    -------
    C : float or array of floats
        Equivalent Celsius temperature(s).

    Notes
    -----
    Computes ``C = (F - 32) / 1.8``.

    Examples
    --------
    >>> from scipy.constants import F2C
    >>> F2C(np.array([-40, 40.0]))
    array([-40.        ,   4.44444444])

    """
    return (_np.asanyarray(F) - 32) / 1.8
