def slice_array(out_name, in_name, blockdims, index):
    """
    Master function for array slicing

    This function makes a new dask that slices blocks along every
    dimension and aggregates (via cartesian product) each dimension's
    slices so that the resulting block slices give the same results
    as the original slice on the original structure

    Index must be a tuple.  It may contain the following types

        int, slice, list (at most one list), None

    Parameters
    ----------
    in_name - string
      This is the dask variable name that will be used as input
    out_name - string
      This is the dask variable output name
    blockshape - iterable of integers
    index - iterable of integers, slices, lists, or None

    Returns
    -------
    Dict where the keys are tuples of

        (out_name, dim_index[, dim_index[, ...]])

    and the values are

        (function, (in_name, dim_index, dim_index, ...),
                   (slice(...), [slice()[,...]])

    Also new blockdims with shapes of each block

        ((10, 10, 10, 10), (20, 20))

    Examples
    --------
    >>> dsk, blockdims = slice_array('y', 'x', [(20, 20, 20, 20, 20)],
    ...                              (slice(10, 35),))  #  doctest: +SKIP
    >>> dsk  # doctest: +SKIP
    {('y', 0): (getitem, ('x', 0), (slice(10, 20),)),
     ('y', 1): (getitem, ('x', 1), (slice(0, 15),))}
    >>> blockdims  # doctest: +SKIP
    ((10, 15),)

    See Also
    --------
    This function works by successively unwrapping cases and passing down
    through a sequence of functions.

    slice_with_newaxis - handle None/newaxis case
    slice_wrap_lists - handle fancy indexing with lists
    slice_slices_and_integers - handle everything else
    """
    blockdims = tuple(map(tuple, blockdims))

    # x[:, :, :] - Punt and return old value
    if all(isinstance(index, slice) and index == slice(None, None, None)
           for index in index):
        suffixes = product(*[range(len(bd)) for bd in blockdims])
        dsk = dict(((out_name,) + s, (in_name,) + s)
                   for s in suffixes)
        return dsk, blockdims

    # Add in missing colons at the end as needed.  x[5] -> x[5, :, :]
    not_none_count = sum(i is not None for i in index)
    missing = len(blockdims) - not_none_count
    index += (slice(None, None, None),) * missing

    # Pass down to next function
    dsk_out, bd_out = slice_with_newaxes(out_name, in_name, blockdims, index)

    bd_out = tuple(map(tuple, bd_out))
    return dsk_out, bd_out
