def str_decode(arr, encoding, errors="strict"):
    """
    Decode character string to unicode using indicated encoding

    Parameters
    ----------
    encoding : string
    errors : string

    Returns
    -------
    decoded : array
    """
    f = lambda x: x.decode(encoding, errors)
    return _na_map(f, arr)
