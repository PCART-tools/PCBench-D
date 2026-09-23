def asanyarray(a):
    """Convert the input to a dask array.

    Subclasses of ``np.ndarray`` will be passed through as chunks unchanged.

    Parameters
    ----------
    a : array-like
        Input data, in any form that can be converted to a dask array.

    Returns
    -------
    out : dask array
        Dask array interpretation of a.

    Examples
    --------
    >>> import dask.array as da
    >>> import numpy as np
    >>> x = np.arange(3)
    >>> da.asanyarray(x)
    dask.array<array, shape=(3,), dtype=int64, chunksize=(3,)>

    >>> y = [[1, 2, 3], [4, 5, 6]]
    >>> da.asanyarray(y)
    dask.array<array, shape=(2, 3), dtype=int64, chunksize=(2, 3)>
    """
    if isinstance(a, Array):
        return a
    if isinstance(a, (list, tuple)) and any(isinstance(i, Array) for i in a):
        a = stack(a)
    elif not isinstance(getattr(a, 'shape', None), Iterable):
        a = np.asanyarray(a)
    return from_array(a, chunks=a.shape, getitem=getter_inline,
                      asarray=False)
