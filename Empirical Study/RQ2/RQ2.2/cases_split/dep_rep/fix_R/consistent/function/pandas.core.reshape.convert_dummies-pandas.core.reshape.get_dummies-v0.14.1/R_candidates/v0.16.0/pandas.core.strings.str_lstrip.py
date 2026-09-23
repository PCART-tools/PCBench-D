def str_lstrip(arr, to_strip=None):
    """
    Strip whitespace (including newlines) from left side of each string in the
    array

    Parameters
    ----------
    to_strip : str or unicode

    Returns
    -------
    stripped : array
    """
    return _na_map(lambda x: x.lstrip(to_strip), arr)
