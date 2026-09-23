@_api.deprecated("3.3", alternative="normalize_kwargs")
def local_over_kwdict(local_var, kwargs, *keys):
    """
    Enforces the priority of a local variable over potentially conflicting
    argument(s) from a kwargs dict. The following possible output values are
    considered in order of priority::

        local_var > kwargs[keys[0]] > ... > kwargs[keys[-1]]

    The first of these whose value is not None will be returned. If all are
    None then None will be returned. Each key in keys will be removed from the
    kwargs dict in place.

    Parameters
    ----------
    local_var : any object
        The local variable (highest priority).

    kwargs : dict
        Dictionary of keyword arguments; modified in place.

    keys : str(s)
        Name(s) of keyword arguments to process, in descending order of
        priority.

    Returns
    -------
    any object
        Either local_var or one of kwargs[key] for key in keys.

    Raises
    ------
    IgnoredKeywordWarning
        For each key in keys that is removed from kwargs but not used as
        the output value.
    """
    return _local_over_kwdict(local_var, kwargs, *keys, IgnoredKeywordWarning)
