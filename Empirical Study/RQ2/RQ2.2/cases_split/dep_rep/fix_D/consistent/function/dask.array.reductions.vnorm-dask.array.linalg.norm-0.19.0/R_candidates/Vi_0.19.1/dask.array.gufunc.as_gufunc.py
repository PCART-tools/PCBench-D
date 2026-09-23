def as_gufunc(signature=None, **kwargs):
    """
    Decorator for ``dask.array.gufunc``.

    Parameters
    ----------
    signature : String
        Specifies what core dimensions are consumed and produced by ``func``.
        According to the specification of numpy.gufunc signature [2]_
    output_dtypes : dtype or list of dtypes, keyword only
        dtype or list of output dtypes.
    output_sizes : dict, optional, keyword only
        Optional mapping from dimension names to sizes for outputs. Only used if
        new core dimensions (not found on inputs) appear on outputs.
    vectorize: bool, keyword only
        If set to ``True``, ``np.vectorize`` is applied to ``func`` for
        convenience. Defaults to ``False``.
    allow_rechunk: Optional, bool, keyword only
        Allows rechunking, otherwise chunk sizes need to match and core
        dimensions are to consist only of one chunk.
        Warning: enabling this can increase memory usage significantly.
        Defaults to ``False``.

    Returns
    -------
    Decorator for `pyfunc` that itself returns a `gufunc`.

    Examples
    --------
    >>> import dask.array as da
    >>> import numpy as np
    >>> a = da.random.normal(size=(10,20,30), chunks=(5, 10, 30))
    >>> @da.as_gufunc("(i)->(),()", output_dtypes=(float, float))
    ... def stats(x):
    ...     return np.mean(x, axis=-1), np.std(x, axis=-1)
    >>> mean, std = stats(a)
    >>> mean.compute().shape
    (10, 20)

    >>> a = da.random.normal(size=(   20,30), chunks=(10, 30))
    >>> b = da.random.normal(size=(10, 1,40), chunks=(5, 1, 40))
    >>> @da.as_gufunc("(i),(j)->(i,j)", output_dtypes=float, vectorize=True)
    ... def outer_product(x, y):
    ...     return np.einsum("i,j->ij", x, y)
    >>> c = outer_product(a, b)
    >>> c.compute().shape
    (10, 20, 30, 40)

    References
    ----------
    .. [1] http://docs.scipy.org/doc/numpy/reference/ufuncs.html
    .. [2] http://docs.scipy.org/doc/numpy/reference/c-api.generalized-ufuncs.html
    """
    _allowedkeys = {"vectorize", "output_sizes", "output_dtypes", "allow_rechunk"}
    if set(_allowedkeys).issubset(kwargs.keys()):
        raise TypeError("Unsupported keyword argument(s) provided")

    def _as_gufunc(pyfunc):
        return gufunc(pyfunc, signature=signature, **kwargs)
    _as_gufunc.__doc__ = """
        Decorator to make ``dask.array.gufunc``
        signature: ``'{signature}'``

        Parameters
        ----------
        pyfunc : callable
            Function matching signature ``'{signature}'``.

        Returns
        -------
        ``dask.array.gufunc``
        """.format(signature=signature)
    return _as_gufunc
