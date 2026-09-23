def slice_with_int_dask_array_on_axis(x, idx, axis):
    """ Slice a ND dask array with a 1D dask arrays of ints along the given
    axis.

    This is a helper function of :func:`slice_with_int_dask_array`.
    """
    from .core import Array, atop, from_array
    from . import chunk

    assert 0 <= axis < x.ndim

    if np.isnan(x.chunks[axis]).any():
        raise NotImplementedError("Slicing an array with unknown chunks with "
                                  "a dask.array of ints is not supported")

    # Calculate the offset at which each chunk starts along axis
    # e.g. chunks=(..., (5, 3, 4), ...) -> offset=[0, 5, 8]
    offset = np.roll(np.cumsum(x.chunks[axis]), 1)
    offset[0] = 0
    offset = from_array(offset, chunks=1)
    # Tamper with the declared chunks of offset to make atop align it with
    # x[axis]
    offset = Array(offset.dask, offset.name, (x.chunks[axis], ), offset.dtype)

    # Define axis labels for atop
    x_axes = tuple(range(x.ndim))
    idx_axes = (x.ndim, )  # arbitrary index not already in x_axes
    offset_axes = (axis, )
    p_axes = x_axes[:axis + 1] + idx_axes + x_axes[axis + 1:]
    y_axes = x_axes[:axis] + idx_axes + x_axes[axis + 1:]

    # Calculate the cartesian product of every chunk of x vs every chunk of idx
    p = atop(chunk.slice_with_int_dask_array,
             p_axes, x, x_axes, idx, idx_axes, offset, offset_axes,
             x_size=x.shape[axis], axis=axis, dtype=x.dtype)

    # Aggregate on the chunks of x along axis
    y = atop(chunk.slice_with_int_dask_array_aggregate,
             y_axes, idx, idx_axes, p, p_axes,
             concatenate=True, x_chunks=x.chunks[axis], axis=axis,
             dtype=x.dtype)
    return y
