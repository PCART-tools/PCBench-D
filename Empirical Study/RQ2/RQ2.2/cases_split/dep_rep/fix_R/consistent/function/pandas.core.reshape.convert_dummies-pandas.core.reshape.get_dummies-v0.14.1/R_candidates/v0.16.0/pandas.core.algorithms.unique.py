def unique(values):
    """
    Compute unique values (not necessarily sorted) efficiently from input array
    of values

    Parameters
    ----------
    values : array-like

    Returns
    -------
    uniques
    """
    values = com._asarray_tuplesafe(values)
    f = lambda htype, caster: _unique_generic(values, htype, caster)
    return _hashtable_algo(f, values.dtype)
