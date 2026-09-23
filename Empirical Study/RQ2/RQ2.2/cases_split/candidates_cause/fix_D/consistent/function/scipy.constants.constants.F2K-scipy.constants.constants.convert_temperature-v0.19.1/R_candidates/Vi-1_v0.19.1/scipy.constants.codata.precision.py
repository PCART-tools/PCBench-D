def precision(key):
    """
    Relative precision in physical_constants indexed by key

    Parameters
    ----------
    key : Python string or unicode
        Key in dictionary `physical_constants`

    Returns
    -------
    prec : float
        Relative precision in `physical_constants` corresponding to `key`

    See Also
    --------
    codata : Contains the description of `physical_constants`, which, as a
        dictionary literal object, does not itself possess a docstring.

    Examples
    --------
    >>> from scipy import constants
    >>> constants.precision(u'proton mass')
    1.2555138746605121e-08

    """
    _check_obsolete(key)
    return physical_constants[key][2] / physical_constants[key][0]
