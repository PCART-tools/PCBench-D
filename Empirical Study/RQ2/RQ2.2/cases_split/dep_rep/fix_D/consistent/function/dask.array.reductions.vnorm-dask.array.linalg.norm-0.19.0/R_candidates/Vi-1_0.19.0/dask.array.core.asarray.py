def asarray(a):
    """Convert the input to a dask array.

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
    >>> da.asarray(x)
    dask.array<array, shape=(3,), dtype=int64, chunksize=(3,)>

    >>> y = [[1, 2, 3], [4, 5, 6]]
    >>> da.asarray(y)
    dask.array<array, shape=(2, 3), dtype=int64, chunksize=(2, 3)>
    """
    try:
        import dask.dataframe as dd
        frame_types = (dd.Series, dd.DataFrame)
    except ImportError:
        frame_types = ()

    if isinstance(a, Array):
        return a
    if isinstance(a, (list, tuple)) and any(isinstance(i, Array) for i in a):
        a = stack(a)
    elif isinstance(a, frame_types):
        return a.to_dask_array()
    elif not isinstance(getattr(a, 'shape', None), Iterable):
        a = np.asarray(a)
    return from_array(a, chunks=a.shape, getitem=getter_inline)
