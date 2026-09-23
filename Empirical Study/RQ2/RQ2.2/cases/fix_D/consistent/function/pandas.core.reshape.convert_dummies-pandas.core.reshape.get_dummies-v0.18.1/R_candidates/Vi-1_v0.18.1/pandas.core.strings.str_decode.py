def str_decode(arr, encoding, errors="strict"):
    """
    Decode character string in the Series/Index using indicated encoding.
    Equivalent to :meth:`str.decode` in python2 and :meth:`bytes.decode` in
    python3.

    Parameters
    ----------
    encoding : str
    errors : str, optional

    Returns
    -------
    decoded : Series/Index of objects
    """
    if encoding in _cpython_optimized_decoders:
        # CPython optimized implementation
        f = lambda x: x.decode(encoding, errors)
    else:
        decoder = codecs.getdecoder(encoding)
        f = lambda x: decoder(x, errors)[0]
    return _na_map(f, arr)
