def str_rstrip(arr, to_strip=None):
    """
    Strip whitespace (including newlines) from right side of each string in the
    array

    Parameters
    ----------
    to_strip : str or unicode

    Returns
    -------
    stripped : array
    """
    return _na_map(lambda x: x.rstrip(to_strip), arr)
