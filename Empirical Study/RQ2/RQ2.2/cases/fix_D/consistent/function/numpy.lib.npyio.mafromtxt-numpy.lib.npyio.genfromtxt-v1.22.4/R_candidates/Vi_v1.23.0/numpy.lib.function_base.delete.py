@array_function_dispatch(_delete_dispatcher)
def delete(arr, obj, axis=None):
    """
    Return a new array with sub-arrays along an axis deleted. For a one
    dimensional array, this returns those entries not returned by
    `arr[obj]`.

    Parameters
    ----------
    arr : array_like
        Input array.
    obj : slice, int or array of ints
        Indicate indices of sub-arrays to remove along the specified axis.

        .. versionchanged:: 1.19.0
            Boolean indices are now treated as a mask of elements to remove,
            rather than being cast to the integers 0 and 1.

    axis : int, optional
        The axis along which to delete the subarray defined by `obj`.
        If `axis` is None, `obj` is applied to the flattened array.

    Returns
    -------
    out : ndarray
        A copy of `arr` with the elements specified by `obj` removed. Note
        that `delete` does not occur in-place. If `axis` is None, `out` is
        a flattened array.

    See Also
    --------
    insert : Insert elements into an array.
    append : Append elements at the end of an array.

    Notes
    -----
    Often it is preferable to use a boolean mask. For example:

    >>> arr = np.arange(12) + 1
    >>> mask = np.ones(len(arr), dtype=bool)
    >>> mask[[0,2,4]] = False
    >>> result = arr[mask,...]

    Is equivalent to ``np.delete(arr, [0,2,4], axis=0)``, but allows further
    use of `mask`.

    Examples
    --------
    >>> arr = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
    >>> arr
    array([[ 1,  2,  3,  4],
           [ 5,  6,  7,  8],
           [ 9, 10, 11, 12]])
    >>> np.delete(arr, 1, 0)
    array([[ 1,  2,  3,  4],
           [ 9, 10, 11, 12]])

    >>> np.delete(arr, np.s_[::2], 1)
    array([[ 2,  4],
           [ 6,  8],
           [10, 12]])
    >>> np.delete(arr, [1,3,5], None)
    array([ 1,  3,  5,  7,  8,  9, 10, 11, 12])

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
        start, stop, step = obj.indices(N)
        xr = range(start, stop, step)
        numtodel = len(xr)

        if numtodel <= 0:
            if wrap:
                return wrap(arr.copy(order=arrorder))
            else:
                return arr.copy(order=arrorder)

        # Invert if step is negative:
        if step < 0:
            step = -step
            start = xr[-1]
            stop = xr[0] + 1

        newshape[axis] -= numtodel
        new = empty(newshape, arr.dtype, arrorder)
        # copy initial chunk
        if start == 0:
            pass
        else:
            slobj[axis] = slice(None, start)
            new[tuple(slobj)] = arr[tuple(slobj)]
        # copy end chunk
        if stop == N:
            pass
        else:
            slobj[axis] = slice(stop-numtodel, None)
            slobj2 = [slice(None)]*ndim
            slobj2[axis] = slice(stop, None)
            new[tuple(slobj)] = arr[tuple(slobj2)]
        # copy middle pieces
        if step == 1:
            pass
        else:  # use array indexing.
            keep = ones(stop-start, dtype=bool)
            keep[:stop-start:step] = False
            slobj[axis] = slice(start, stop-numtodel)
            slobj2 = [slice(None)]*ndim
            slobj2[axis] = slice(start, stop)
            arr = arr[tuple(slobj2)]
            slobj2[axis] = keep
            new[tuple(slobj)] = arr[tuple(slobj2)]
        if wrap:
            return wrap(new)
        else:
            return new

    if isinstance(obj, (int, integer)) and not isinstance(obj, bool):
        single_value = True
    else:
        single_value = False
        _obj = obj
        obj = np.asarray(obj)
        if obj.size == 0 and not isinstance(_obj, np.ndarray):
            obj = obj.astype(intp)
        elif obj.size == 1 and not isinstance(_obj, bool):
            obj = obj.astype(intp).reshape(())
            single_value = True

    if single_value:
        # optimization for a single value
        if (obj < -N or obj >= N):
            raise IndexError(
                "index %i is out of bounds for axis %i with "
                "size %i" % (obj, axis, N))
        if (obj < 0):
            obj += N
        newshape[axis] -= 1
        new = empty(newshape, arr.dtype, arrorder)
        slobj[axis] = slice(None, obj)
        new[tuple(slobj)] = arr[tuple(slobj)]
        slobj[axis] = slice(obj, None)
        slobj2 = [slice(None)]*ndim
        slobj2[axis] = slice(obj+1, None)
        new[tuple(slobj)] = arr[tuple(slobj2)]
    else:
        if obj.dtype == bool:
            if obj.shape != (N,):
                raise ValueError('boolean array argument obj to delete '
                                 'must be one dimensional and match the axis '
                                 'length of {}'.format(N))

            # optimization, the other branch is slower
            keep = ~obj
        else:
            keep = ones(N, dtype=bool)
            keep[obj,] = False

        slobj[axis] = keep
        new = arr[tuple(slobj)]

    if wrap:
        return wrap(new)
    else:
        return new
