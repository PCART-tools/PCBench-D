def full_like(a, fill_value, dtype=None, chunks=None):
    """
    Return a full array with the same shape and type as a given array.

    Parameters
    ----------
    a : array_like
        The shape and data-type of `a` define these same attributes of
        the returned array.
    fill_value : scalar
        Fill value.
    dtype : data-type, optional
        Overrides the data type of the result.
    chunks : sequence of ints
        The number of samples on each block. Note that the last block will have
        fewer samples if ``len(array) % chunks != 0``.

    Returns
    -------
    out : ndarray
        Array of `fill_value` with the same shape and type as `a`.

    See Also
    --------
    zeros_like : Return an array of zeros with shape and type of input.
    ones_like : Return an array of ones with shape and type of input.
    empty_like : Return an empty array with shape and type of input.
    zeros : Return a new array setting values to zero.
    ones : Return a new array setting values to one.
    empty : Return a new uninitialized array.
    full : Fill a new array.
    """

    a = asarray(a)
    return full(
        a.shape,
        fill_value,
        dtype=(dtype or a.dtype),
        chunks=(chunks if chunks is not None else a.chunks)
    )
