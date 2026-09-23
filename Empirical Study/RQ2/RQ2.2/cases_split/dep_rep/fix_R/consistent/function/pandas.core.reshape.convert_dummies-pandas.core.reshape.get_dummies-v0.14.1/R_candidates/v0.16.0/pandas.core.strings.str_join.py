def str_join(arr, sep):
    """
    Join lists contained as elements in array, a la str.join

    Parameters
    ----------
    sep : string
        Delimiter

    Returns
    -------
    joined : array
    """
    return _na_map(sep.join, arr)
