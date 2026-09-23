def retrieve_from_ooc(keys, dsk_pre, dsk_post=None):
    """
    Creates a Dask graph for loading stored ``keys`` from ``dsk``.

    Parameters
    ----------
    keys: Sequence
        A sequence containing Dask graph keys to load
    dsk_pre: Mapping
        A Dask graph corresponding to a Dask Array before computation
    dsk_post: Mapping, optional
        A Dask graph corresponding to a Dask Array after computation

    Examples
    --------
    >>> import dask.array as da
    >>> d = da.ones((5, 6), chunks=(2, 3))
    >>> a = np.empty(d.shape)
    >>> g = insert_to_ooc(d, a)
    >>> retrieve_from_ooc(g.keys(), g)  # doctest: +SKIP
    """

    if not dsk_post:
        dsk_post = {k: k for k in keys}

    load_dsk = {
        ('load-' + k[0],) + k[1:]: (load_chunk, dsk_post[k]) + dsk_pre[k][3:-1]
        for k in keys
    }

    return load_dsk
