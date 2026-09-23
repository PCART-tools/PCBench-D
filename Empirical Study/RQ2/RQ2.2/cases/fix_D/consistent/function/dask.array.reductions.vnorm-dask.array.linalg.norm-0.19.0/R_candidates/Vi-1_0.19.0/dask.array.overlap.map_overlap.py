def map_overlap(x, func, depth, boundary=None, trim=True, **kwargs):
    """ Map a function over blocks of the array with some overlap

    We share neighboring zones between blocks of the array, then map a
    function, then trim away the neighboring strips.

    Parameters
    ----------
    func: function
        The function to apply to each extended block
    depth: int, tuple, or dict
        The number of elements that each block should share with its neighbors
        If a tuple or dict then this can be different per axis
    boundary: str, tuple, dict
        How to handle the boundaries.
        Values include 'reflect', 'periodic', 'nearest', 'none',
        or any constant value like 0 or np.nan
    trim: bool
        Whether or not to trim ``depth`` elements from each block after
        calling the map function.
        Set this to False if your mapping function already does this for you
    **kwargs:
        Other keyword arguments valid in ``map_blocks``

    Examples
    --------
    >>> import numpy as np
    >>> import dask.array as da

    >>> x = np.array([1, 1, 2, 3, 3, 3, 2, 1, 1])
    >>> x = da.from_array(x, chunks=5)
    >>> def derivative(x):
    ...     return x - np.roll(x, 1)

    >>> y = x.map_overlap(derivative, depth=1, boundary=0)
    >>> y.compute()
    array([ 1,  0,  1,  1,  0,  0, -1, -1,  0])

    >>> x = np.arange(16).reshape((4, 4))
    >>> d = da.from_array(x, chunks=(2, 2))
    >>> d.map_overlap(lambda x: x + x.size, depth=1).compute()
    array([[16, 17, 18, 19],
           [20, 21, 22, 23],
           [24, 25, 26, 27],
           [28, 29, 30, 31]])

    >>> func = lambda x: x + x.size
    >>> depth = {0: 1, 1: 1}
    >>> boundary = {0: 'reflect', 1: 'none'}
    >>> d.map_overlap(func, depth, boundary).compute()  # doctest: +NORMALIZE_WHITESPACE
    array([[12,  13,  14,  15],
           [16,  17,  18,  19],
           [20,  21,  22,  23],
           [24,  25,  26,  27]])
    """
    depth2 = coerce_depth(x.ndim, depth)
    boundary2 = coerce_boundary(x.ndim, boundary)

    g = overlap(x, depth=depth2, boundary=boundary2)
    g2 = g.map_blocks(func, **kwargs)
    if trim:
        g3 = add_dummy_padding(g2, depth2, boundary2)
        return trim_internal(g3, depth2)
    else:
        return g2
