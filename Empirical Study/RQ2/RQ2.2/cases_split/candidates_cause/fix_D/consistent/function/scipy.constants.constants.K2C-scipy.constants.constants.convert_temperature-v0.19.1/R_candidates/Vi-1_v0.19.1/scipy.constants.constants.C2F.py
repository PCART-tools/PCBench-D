@_np.deprecate(message="scipy.constants.C2F is deprecated in scipy 0.18.0. "
                       "Use scipy.constants.convert_temperature instead. "
                       "Note that the new function has a different signature.")
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

    See also
    --------
    convert_temperature

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
