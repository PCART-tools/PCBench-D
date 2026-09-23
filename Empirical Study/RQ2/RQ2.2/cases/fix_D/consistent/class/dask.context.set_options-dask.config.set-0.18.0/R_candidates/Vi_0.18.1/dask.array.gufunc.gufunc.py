class gufunc(object):
    """
    Binds `pyfunc` into ``dask.array.apply_gufunc`` when called.

    Parameters
    ----------
    pyfunc : callable
        Function to call like ``func(*args, **kwargs)`` on input arrays
        (``*args``) that returns an array or tuple of arrays. If multiple
        arguments with non-matching dimensions are supplied, this function is
        expected to vectorize (broadcast) over axes of positional arguments in
        the style of NumPy universal functions [1]_ (if this is not the case,
        set ``vectorize=True``). If this function returns multiple outputs,
        ``output_core_dims`` has to be set as well.
    signature : String, keyword only
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
    Wrapped function

    Examples
    --------
    >>> import dask.array as da
    >>> import numpy as np
    >>> a = da.random.normal(size=(10,20,30), chunks=(5, 10, 30))
    >>> def stats(x):
    ...     return np.mean(x, axis=-1), np.std(x, axis=-1)
    >>> gustats = da.gufunc(stats, signature="(i)->(),()", output_dtypes=(float, float))
    >>> mean, std = gustats(a)
    >>> mean.compute().shape
    (10, 20)


    >>> a = da.random.normal(size=(   20,30), chunks=(10, 30))
    >>> b = da.random.normal(size=(10, 1,40), chunks=(5, 1, 40))
    >>> def outer_product(x, y):
    ...     return np.einsum("i,j->ij", x, y)
    >>> guouter_product = da.gufunc(outer_product, signature="(i),(j)->(i,j)", output_dtypes=float, vectorize=True)
    >>> c = guouter_product(a, b)
    >>> c.compute().shape
    (10, 20, 30, 40)

    References
    ----------
    .. [1] http://docs.scipy.org/doc/numpy/reference/ufuncs.html
    .. [2] http://docs.scipy.org/doc/numpy/reference/c-api.generalized-ufuncs.html
    """
    def __init__(self, pyfunc, **kwargs):
        self.pyfunc = pyfunc
        self.signature = kwargs.pop("signature", None)
        self.vectorize = kwargs.pop("vectorize", False)
        self.output_sizes = kwargs.pop("output_sizes", None)
        self.output_dtypes = kwargs.pop("output_dtypes", None)
        self.allow_rechunk = kwargs.pop("allow_rechunk", False)
        if kwargs:
            raise TypeError("Unsupported keyword argument(s) provided")

        self.__doc__ = """
        Bound ``dask.array.gufunc``
        func: ``{func}``
        signature: ``'{signature}'``

        Parameters
        ----------
        *args : numpy/dask arrays or scalars
            Arrays to which to apply to ``func``. Core dimensions as specified in
            ``signature`` need to come last.
        **kwargs : dict
            Extra keyword arguments to pass to ``func``

        Returns
        -------
        Single dask.array.Array or tuple of dask.array.Array
        """.format(func=str(self.pyfunc), signature=self.signature)

    def __call__(self, *args, **kwargs):
        return apply_gufunc(self.pyfunc,
                            self.signature,
                            *args,
                            vectorize=self.vectorize,
                            output_sizes=self.output_sizes,
                            output_dtypes=self.output_dtypes,
                            allow_rechunk=self.allow_rechunk or kwargs.pop("allow_rechunk", False),
                            **kwargs)
