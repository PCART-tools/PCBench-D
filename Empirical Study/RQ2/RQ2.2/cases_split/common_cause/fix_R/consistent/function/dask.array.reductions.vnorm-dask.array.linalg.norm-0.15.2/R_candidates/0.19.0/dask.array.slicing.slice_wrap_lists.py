def slice_wrap_lists(out_name, in_name, blockdims, index):
    """
    Fancy indexing along blocked array dasks

    Handles index of type list.  Calls slice_slices_and_integers for the rest

    See Also
    --------

    take - handle slicing with lists ("fancy" indexing)
    slice_slices_and_integers - handle slicing with slices and integers
    """
    assert all(isinstance(i, (slice, list, Integral, np.ndarray))
               for i in index)
    if not len(blockdims) == len(index):
        raise IndexError("Too many indices for array")

    # Do we have more than one list in the index?
    where_list = [i for i, ind in enumerate(index)
                  if isinstance(ind, np.ndarray) and ind.ndim > 0]
    if len(where_list) > 1:
        raise NotImplementedError("Don't yet support nd fancy indexing")
    # Is the single list an empty list? In this case just treat it as a zero
    # length slice
    if where_list and not index[where_list[0]].size:
        index = list(index)
        index[where_list.pop()] = slice(0, 0, 1)
        index = tuple(index)

    # No lists, hooray! just use slice_slices_and_integers
    if not where_list:
        return slice_slices_and_integers(out_name, in_name, blockdims, index)

    # Replace all lists with full slices  [3, 1, 0] -> slice(None, None, None)
    index_without_list = tuple(slice(None, None, None)
                               if isinstance(i, np.ndarray) else i
                               for i in index)

    # lists and full slices.  Just use take
    if all(isinstance(i, np.ndarray) or i == slice(None, None, None)
           for i in index):
        axis = where_list[0]
        blockdims2, dsk3 = take(out_name, in_name, blockdims,
                                index[where_list[0]], axis=axis)
    # Mixed case. Both slices/integers and lists. slice/integer then take
    else:
        # Do first pass without lists
        tmp = 'slice-' + tokenize((out_name, in_name, blockdims, index))
        dsk, blockdims2 = slice_slices_and_integers(tmp, in_name, blockdims, index_without_list)

        # After collapsing some axes due to int indices, adjust axis parameter
        axis = where_list[0]
        axis2 = axis - sum(1 for i, ind in enumerate(index)
                           if i < axis and isinstance(ind, Integral))

        # Do work
        blockdims2, dsk2 = take(out_name, tmp, blockdims2, index[axis],
                                axis=axis2)
        dsk3 = merge(dsk, dsk2)

    return dsk3, blockdims2
