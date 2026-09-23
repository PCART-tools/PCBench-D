@_np.deprecate(message="scipy.constants.C2K is deprecated in scipy 0.18.0. "
                       "Use scipy.constants.convert_temperature instead. "
                       "Note that the new function has a different signature.")
def C2K(C):
    """
    Convert Celsius to Kelvin

    Parameters
    ----------
    C : array_like
        Celsius temperature(s) to be converted.

    Returns
    -------
    K : float or array of floats
        Equivalent Kelvin temperature(s).

    See also
    --------
    convert_temperature

    Notes
    -----
    Computes ``K = C + zero_Celsius`` where `zero_Celsius` = 273.15, i.e.,
    (the absolute value of) temperature "absolute zero" as measured in Celsius.

    Examples
    --------
    >>> from scipy.constants import C2K
    >>> C2K(np.array([-40, 40.0]))
    array([ 233.15,  313.15])

    """
    return _np.asanyarray(C) + zero_Celsius
