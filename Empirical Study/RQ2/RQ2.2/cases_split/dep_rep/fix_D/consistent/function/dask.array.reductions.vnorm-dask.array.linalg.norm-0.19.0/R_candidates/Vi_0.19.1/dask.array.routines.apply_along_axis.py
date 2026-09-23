@wraps(np.apply_along_axis)
def apply_along_axis(func1d, axis, arr, *args, **kwargs):
    arr = asarray(arr)

    # Validate and normalize axis.
    arr.shape[axis]
    axis = len(arr.shape[:axis])

    # Test out some data with the function.
    test_data = np.ones((1,), dtype=arr.dtype)
    test_result = np.array(func1d(test_data, *args, **kwargs))

    if (LooseVersion(np.__version__) < LooseVersion("1.13.0") and
            (np.array(test_result.shape) > 1).sum(dtype=int) > 1):
        raise ValueError(
            "No more than one non-trivial dimension allowed in result. "
            "Need NumPy 1.13.0+ for this functionality."
        )

    # Rechunk so that func1d is applied over the full axis.
    arr = arr.rechunk(
        arr.chunks[:axis] + (arr.shape[axis:axis + 1],) + arr.chunks[axis + 1:]
    )

    # Map func1d over the data to get the result
    # Adds other axes as needed.
    result = arr.map_blocks(
        _inner_apply_along_axis,
        name=funcname(func1d) + '-along-axis',
        dtype=test_result.dtype,
        chunks=(arr.chunks[:axis] + test_result.shape + arr.chunks[axis + 1:]),
        drop_axis=axis,
        new_axis=list(range(axis, axis + test_result.ndim, 1)),
        func1d=func1d,
        func1d_axis=axis,
        func1d_args=args,
        func1d_kwargs=kwargs,
    )

    return result
