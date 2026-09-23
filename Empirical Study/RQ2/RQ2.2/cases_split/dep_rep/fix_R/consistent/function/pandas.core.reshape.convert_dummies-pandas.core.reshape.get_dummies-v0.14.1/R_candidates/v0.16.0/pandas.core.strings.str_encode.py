def str_encode(arr, encoding, errors="strict"):
    """
    Encode character string to some other encoding using indicated encoding

    Parameters
    ----------
    encoding : string
    errors : string

    Returns
    -------
    encoded : array
    """
    f = lambda x: x.encode(encoding, errors)
    return _na_map(f, arr)
