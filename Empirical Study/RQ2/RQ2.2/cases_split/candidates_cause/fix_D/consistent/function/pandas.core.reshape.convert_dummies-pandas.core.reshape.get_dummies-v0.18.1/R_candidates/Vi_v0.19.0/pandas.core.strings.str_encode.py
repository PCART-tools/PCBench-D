def str_encode(arr, encoding, errors="strict"):
    """
    Encode character string in the Series/Index using indicated encoding.
    Equivalent to :meth:`str.encode`.

    Parameters
    ----------
    encoding : str
    errors : str, optional

    Returns
    -------
    encoded : Series/Index of objects
    """
    if encoding in _cpython_optimized_encoders:
        # CPython optimized implementation
        f = lambda x: x.encode(encoding, errors)
    else:
        encoder = codecs.getencoder(encoding)
        f = lambda x: encoder(x, errors)[0]
    return _na_map(f, arr)
