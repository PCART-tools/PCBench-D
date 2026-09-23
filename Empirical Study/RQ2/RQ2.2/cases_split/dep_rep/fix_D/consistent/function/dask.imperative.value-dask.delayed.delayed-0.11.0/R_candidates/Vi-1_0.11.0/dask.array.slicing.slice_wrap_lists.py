def slice_wrap_lists(out_name, in_name, blockdims, index):
    """
    Fancy indexing along blocked array dasks

    Handles index of type list.  Calls slice_slices_and_integers for the rest

    See Also
    --------

    take - handle slicing with lists ("fancy" indexing)
    slice_slices_and_integers - handle slicing with slices and integers
    """
    shape = tuple(map(sum, blockdims))
    assert all(isinstance(i, (slice, list, int, long)) for i in index)
    assert len(blockdims) == len(index)
    for bd, i in zip(blockdims, index):
        check_index(i, sum(bd))

    # Change indices like -1 to 9
    index2 = posify_index(shape, index)

    # Do we have more than one list in the index?
    where_list = [i for i, ind in enumerate(index) if isinstance(ind, list)]
    if len(where_list) > 1:
        raise NotImplementedError("Don't yet support nd fancy indexing")

    # Replace all lists with full slices  [3, 1, 0] -> slice(None, None, None)
    index_without_list = tuple(slice(None, None, None)
                                    if isinstance(i, list)
                                    else i
                                    for i in index2)

    # No lists, hooray! just use slice_slices_and_integers
    if index2 == index_without_list:
        return slice_slices_and_integers(out_name, in_name, blockdims, index2)

    # lists and full slices.  Just use take
    if all(isinstance(i, list) or i == slice(None, None, None)
            for i in index2):
        axis = where_list[0]
        blockdims2, dsk3 = take(out_name, in_name, blockdims,
                                index2[where_list[0]], axis=axis)
    # Mixed case. Both slices/integers and lists. slice/integer then take
    else:
        # Do first pass without lists
        tmp = 'slice-' + tokenize((out_name, in_name, blockdims, index))
        dsk, blockdims2 = slice_slices_and_integers(tmp, in_name, blockdims, index_without_list)

        # After collapsing some axes due to int indices, adjust axis parameter
        axis = where_list[0]
        axis2 = axis - sum(1 for i, ind in enumerate(index2)
                           if i < axis and isinstance(ind, (int, long)))

        # Do work
        blockdims2, dsk2 = take(out_name, tmp, blockdims2, index2[axis],
                                axis=axis2)
        dsk3 = merge(dsk, dsk2)

    return dsk3, blockdims2
