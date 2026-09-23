@_np.deprecate(message="scipy.constants.K2C is deprecated in scipy 0.18.0. "
                       "Use scipy.constants.convert_temperature instead. "
                       "Note that the new function has a different signature.")
def K2C(K):
    """
    Convert Kelvin to Celsius

    Parameters
    ----------
    K : array_like
        Kelvin temperature(s) to be converted.

    Returns
    -------
    C : float or array of floats
        Equivalent Celsius temperature(s).

    See also
    --------
    convert_temperature

    Notes
    -----
    Computes ``C = K - zero_Celsius`` where `zero_Celsius` = 273.15, i.e.,
    (the absolute value of) temperature "absolute zero" as measured in Celsius.

    Examples
    --------
    >>> from scipy.constants import K2C
    >>> K2C(np.array([233.15, 313.15]))
    array([-40.,  40.])

    """
    return _np.asanyarray(K) - zero_Celsius
