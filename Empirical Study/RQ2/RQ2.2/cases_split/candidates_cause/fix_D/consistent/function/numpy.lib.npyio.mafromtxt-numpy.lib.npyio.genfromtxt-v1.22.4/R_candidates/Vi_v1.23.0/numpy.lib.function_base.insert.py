@array_function_dispatch(_insert_dispatcher)
def insert(arr, obj, values, axis=None):
    """
    Insert values along the given axis before the given indices.

    Parameters
    ----------
    arr : array_like
        Input array.
    obj : int, slice or sequence of ints
        Object that defines the index or indices before which `values` is
        inserted.

        .. versionadded:: 1.8.0

        Support for multiple insertions when `obj` is a single scalar or a
        sequence with one element (similar to calling insert multiple
        times).
    values : array_like
        Values to insert into `arr`. If the type of `values` is different
        from that of `arr`, `values` is converted to the type of `arr`.
        `values` should be shaped so that ``arr[...,obj,...] = values``
        is legal.
    axis : int, optional
        Axis along which to insert `values`.  If `axis` is None then `arr`
        is flattened first.

    Returns
    -------
    out : ndarray
        A copy of `arr` with `values` inserted.  Note that `insert`
        does not occur in-place: a new array is returned. If
        `axis` is None, `out` is a flattened array.

    See Also
    --------
    append : Append elements at the end of an array.
    concatenate : Join a sequence of arrays along an existing axis.
    delete : Delete elements from an array.

    Notes
    -----
    Note that for higher dimensional inserts ``obj=0`` behaves very different
    from ``obj=[0]`` just like ``arr[:,0,:] = values`` is different from
    ``arr[:,[0],:] = values``.

    Examples
    --------
    >>> a = np.array([[1, 1], [2, 2], [3, 3]])
    >>> a
    array([[1, 1],
           [2, 2],
           [3, 3]])
    >>> np.insert(a, 1, 5)
    array([1, 5, 1, ..., 2, 3, 3])
    >>> np.insert(a, 1, 5, axis=1)
    array([[1, 5, 1],
           [2, 5, 2],
           [3, 5, 3]])

    Difference between sequence and scalars:

    >>> np.insert(a, [1], [[1],[2],[3]], axis=1)
    array([[1, 1, 1],
           [2, 2, 2],
           [3, 3, 3]])
    >>> np.array_equal(np.insert(a, 1, [1, 2, 3], axis=1),
    ...                np.insert(a, [1], [[1],[2],[3]], axis=1))
    True

    >>> b = a.flatten()
    >>> b
    array([1, 1, 2, 2, 3, 3])
    >>> np.insert(b, [2, 2], [5, 6])
    array([1, 1, 5, ..., 2, 3, 3])

    >>> np.insert(b, slice(2, 4), [5, 6])
    array([1, 1, 5, ..., 2, 3, 3])

    >>> np.insert(b, [2, 2], [7.13, False]) # type casting
    array([1, 1, 7, ..., 2, 3, 3])

    >>> x = np.arange(8).reshape(2, 4)
    >>> idx = (1, 3)
    >>> np.insert(x, idx, 999, axis=1)
    array([[  0, 999,   1,   2, 999,   3],
           [  4, 999,   5,   6, 999,   7]])

    """
    wrap = None
    if type(arr) is not ndarray:
        try:
            wrap = arr.__array_wrap__
        except AttributeError:
            pass

    arr = asarray(arr)
    ndim = arr.ndim
    arrorder = 'F' if arr.flags.fnc else 'C'
    if axis is None:
        if ndim != 1:
            arr = arr.ravel()
        # needed for np.matrix, which is still not 1d after being ravelled
        ndim = arr.ndim
        axis = ndim - 1
    else:
        axis = normalize_axis_index(axis, ndim)
    slobj = [slice(None)]*ndim
    N = arr.shape[axis]
    newshape = list(arr.shape)

    if isinstance(obj, slice):
        # turn it into a range object
        indices = arange(*obj.indices(N), dtype=intp)
    else:
        # need to copy obj, because indices will be changed in-place
        indices = np.array(obj)
        if indices.dtype == bool:
            # See also delete
            # 2012-10-11, NumPy 1.8
            warnings.warn(
                "in the future insert will treat boolean arrays and "
                "array-likes as a boolean index instead of casting it to "
                "integer", FutureWarning, stacklevel=3)
            indices = indices.astype(intp)
            # Code after warning period:
            #if obj.ndim != 1:
            #    raise ValueError('boolean array argument obj to insert '
            #                     'must be one dimensional')
            #indices = np.flatnonzero(obj)
        elif indices.ndim > 1:
            raise ValueError(
                "index array argument obj to insert must be one dimensional "
                "or scalar")
    if indices.size == 1:
        index = indices.item()
        if index < -N or index > N:
            raise IndexError(f"index {obj} is out of bounds for axis {axis} "
                             f"with size {N}")
        if (index < 0):
            index += N

        # There are some object array corner cases here, but we cannot avoid
        # that:
        values = array(values, copy=False, ndmin=arr.ndim, dtype=arr.dtype)
        if indices.ndim == 0:
            # broadcasting is very different here, since a[:,0,:] = ... behaves
            # very different from a[:,[0],:] = ...! This changes values so that
            # it works likes the second case. (here a[:,0:1,:])
            values = np.moveaxis(values, 0, axis)
        numnew = values.shape[axis]
        newshape[axis] += numnew
        new = empty(newshape, arr.dtype, arrorder)
        slobj[axis] = slice(None, index)
        new[tuple(slobj)] = arr[tuple(slobj)]
        slobj[axis] = slice(index, index+numnew)
        new[tuple(slobj)] = values
        slobj[axis] = slice(index+numnew, None)
        slobj2 = [slice(None)] * ndim
        slobj2[axis] = slice(index, None)
        new[tuple(slobj)] = arr[tuple(slobj2)]
        if wrap:
            return wrap(new)
        return new
    elif indices.size == 0 and not isinstance(obj, np.ndarray):
        # Can safely cast the empty list to intp
        indices = indices.astype(intp)

    indices[indices < 0] += N

    numnew = len(indices)
    order = indices.argsort(kind='mergesort')   # stable sort
    indices[order] += np.arange(numnew)

    newshape[axis] += numnew
    old_mask = ones(newshape[axis], dtype=bool)
    old_mask[indices] = False

    new = empty(newshape, arr.dtype, arrorder)
    slobj2 = [slice(None)]*ndim
    slobj[axis] = indices
    slobj2[axis] = old_mask
    new[tuple(slobj)] = values
    new[tuple(slobj2)] = arr

    if wrap:
        return wrap(new)
    return new
