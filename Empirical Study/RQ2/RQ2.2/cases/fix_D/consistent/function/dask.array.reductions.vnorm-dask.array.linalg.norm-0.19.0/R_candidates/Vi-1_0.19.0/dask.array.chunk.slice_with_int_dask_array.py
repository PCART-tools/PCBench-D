def slice_with_int_dask_array(x, idx, offset, x_size, axis):
    """ Chunk function of `slice_with_int_dask_array_on_axis`.
    Slice one chunk of x by one chunk of idx.

    Parameters
    ----------
    x: ndarray, any dtype, any shape
        i-th chunk of x
    idx: ndarray, ndim=1, dtype=any integer
        j-th chunk of idx (cartesian product with the chunks of x)
    offset: ndarray, shape=(1, ), dtype=int64
        Index of the first element along axis of the current chunk of x
    x_size: int
        Total size of the x da.Array along axis
    axis: int
        normalized axis to take elements from (0 <= axis < x.ndim)

    Returns
    -------
    x sliced along axis, using only the elements of idx that fall inside the
    current chunk.
    """
    # Needed when idx is unsigned
    idx = idx.astype(np.int64)

    # Normalize negative indices
    idx = np.where(idx < 0, idx + x_size, idx)

    # A chunk of the offset dask Array is a numpy array with shape (1, ).
    # It indicates the index of the first element along axis of the current
    # chunk of x.
    idx = idx - offset

    # Drop elements of idx that do not fall inside the current chunk of x
    idx_filter = (idx >= 0) & (idx < x.shape[axis])
    idx = idx[idx_filter]

    # np.take does not support slice indices
    # return np.take(x, idx, axis)
    return x[tuple(
        idx if i == axis else slice(None)
        for i in range(x.ndim)
    )]
