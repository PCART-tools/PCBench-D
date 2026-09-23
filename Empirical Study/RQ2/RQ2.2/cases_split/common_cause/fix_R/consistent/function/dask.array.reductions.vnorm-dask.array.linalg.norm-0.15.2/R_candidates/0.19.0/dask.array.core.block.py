def block(arrays, allow_unknown_chunksizes=False):
    """
    Assemble an nd-array from nested lists of blocks.

    Blocks in the innermost lists are concatenated along the last
    dimension (-1), then these are concatenated along the second-last
    dimension (-2), and so on until the outermost list is reached

    Blocks can be of any dimension, but will not be broadcasted using the normal
    rules. Instead, leading axes of size 1 are inserted, to make ``block.ndim``
    the same for all blocks. This is primarily useful for working with scalars,
    and means that code like ``block([v, 1])`` is valid, where
    ``v.ndim == 1``.

    When the nested list is two levels deep, this allows block matrices to be
    constructed from their components.

    Parameters
    ----------
    arrays : nested list of array_like or scalars (but not tuples)
        If passed a single ndarray or scalar (a nested list of depth 0), this
        is returned unmodified (and not copied).

        Elements shapes must match along the appropriate axes (without
        broadcasting), but leading 1s will be prepended to the shape as
        necessary to make the dimensions match.

    allow_unknown_chunksizes: bool
        Allow unknown chunksizes, such as come from converting from dask
        dataframes.  Dask.array is unable to verify that chunks line up.  If
        data comes from differently aligned sources then this can cause
        unexpected results.

    Returns
    -------
    block_array : ndarray
        The array assembled from the given blocks.

        The dimensionality of the output is equal to the greatest of:
        * the dimensionality of all the inputs
        * the depth to which the input list is nested

    Raises
    ------
    ValueError
        * If list depths are mismatched - for instance, ``[[a, b], c]`` is
          illegal, and should be spelt ``[[a, b], [c]]``
        * If lists are empty - for instance, ``[[a, b], []]``

    See Also
    --------
    concatenate : Join a sequence of arrays together.
    stack : Stack arrays in sequence along a new dimension.
    hstack : Stack arrays in sequence horizontally (column wise).
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third dimension).
    vsplit : Split array into a list of multiple sub-arrays vertically.

    Notes
    -----

    When called with only scalars, ``block`` is equivalent to an ndarray
    call. So ``block([[1, 2], [3, 4]])`` is equivalent to
    ``array([[1, 2], [3, 4]])``.

    This function does not enforce that the blocks lie on a fixed grid.
    ``block([[a, b], [c, d]])`` is not restricted to arrays of the form::

        AAAbb
        AAAbb
        cccDD

    But is also allowed to produce, for some ``a, b, c, d``::

        AAAbb
        AAAbb
        cDDDD

    Since concatenation happens along the last axis first, `block` is _not_
    capable of producing the following directly::

        AAAbb
        cccbb
        cccDD

    Matlab's "square bracket stacking", ``[A, B, ...; p, q, ...]``, is
    equivalent to ``block([[A, B, ...], [p, q, ...]])``.
    """

    # This was copied almost verbatim from numpy.core.shape_base.block
    # See numpy license at https://github.com/numpy/numpy/blob/master/LICENSE.txt
    # or NUMPY_LICENSE.txt within this directory

    def atleast_nd(x, ndim):
        x = asanyarray(x)
        diff = max(ndim - x.ndim, 0)
        return x[(None,) * diff + (Ellipsis,)]

    def format_index(index):
        return 'arrays' + ''.join('[{}]'.format(i) for i in index)

    rec = _Recurser(recurse_if=lambda x: type(x) is list)

    # ensure that the lists are all matched in depth
    list_ndim = None
    any_empty = False
    for index, value, entering in rec.walk(arrays):
        if type(value) is tuple:
            # not strictly necessary, but saves us from:
            #  - more than one way to do things - no point treating tuples like
            #    lists
            #  - horribly confusing behaviour that results when tuples are
            #    treated like ndarray
            raise TypeError(
                '{} is a tuple. '
                'Only lists can be used to arrange blocks, and np.block does '
                'not allow implicit conversion from tuple to ndarray.'.format(
                    format_index(index)
                )
            )
        if not entering:
            curr_depth = len(index)
        elif len(value) == 0:
            curr_depth = len(index) + 1
            any_empty = True
        else:
            continue

        if list_ndim is not None and list_ndim != curr_depth:
            raise ValueError(
                "List depths are mismatched. First element was at depth {}, "
                "but there is an element at depth {} ({})".format(
                    list_ndim,
                    curr_depth,
                    format_index(index)
                )
            )
        list_ndim = curr_depth

    # do this here so we catch depth mismatches first
    if any_empty:
        raise ValueError('Lists cannot be empty')

    # convert all the arrays to ndarrays
    arrays = rec.map_reduce(
        arrays,
        f_map=asanyarray,
        f_reduce=list
    )

    # determine the maximum dimension of the elements
    elem_ndim = rec.map_reduce(
        arrays,
        f_map=lambda xi: xi.ndim,
        f_reduce=max
    )
    ndim = max(list_ndim, elem_ndim)

    # first axis to concatenate along
    first_axis = ndim - list_ndim

    # Make all the elements the same dimension
    arrays = rec.map_reduce(
        arrays,
        f_map=lambda xi: atleast_nd(xi, ndim),
        f_reduce=list
    )

    # concatenate innermost lists on the right, outermost on the left
    return rec.map_reduce(
        arrays,
        f_reduce=lambda xs, axis: concatenate(
            list(xs),
            axis=axis,
            allow_unknown_chunksizes=allow_unknown_chunksizes
        ),
        f_kwargs=lambda axis: dict(axis=(axis + 1)),
        axis=first_axis
    )
