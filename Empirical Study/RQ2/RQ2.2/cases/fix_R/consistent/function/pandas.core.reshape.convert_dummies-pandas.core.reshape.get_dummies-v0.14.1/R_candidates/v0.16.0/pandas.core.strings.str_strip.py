def str_strip(arr, to_strip=None):
    """
    Strip whitespace (including newlines) from each string in the array

    Parameters
    ----------
    to_strip : str or unicode

    Returns
    -------
    stripped : array
    """
    return _na_map(lambda x: x.strip(to_strip), arr)
