def elemwise(op, *args, **kwargs):
    """ Apply elementwise function across arguments

    Respects broadcasting rules

    Examples
    --------
    >>> elemwise(add, x, y)  # doctest: +SKIP
    >>> elemwise(sin, x)  # doctest: +SKIP

    See Also
    --------
    atop
    """
    if not set(['name', 'dtype']).issuperset(kwargs):
        msg = "%s does not take the following keyword arguments %s"
        raise TypeError(msg % (op.__name__, str(sorted(set(kwargs) - set(['name', 'dtype'])))))

    shapes = [getattr(arg, 'shape', ()) for arg in args]
    shapes = [s if isinstance(s, Iterable) else () for s in shapes]
    out_ndim = len(broadcast_shapes(*shapes))   # Raises ValueError if dimensions mismatch
    expr_inds = tuple(range(out_ndim))[::-1]

    arrays = [asarray(a) for a in args if not is_scalar_for_elemwise(a)]
    other = [(i, a) for i, a in enumerate(args) if is_scalar_for_elemwise(a)]

    if 'dtype' in kwargs:
        dt = kwargs['dtype']
    elif any(a._dtype is None for a in arrays):
        dt = None
    else:
        # We follow NumPy's rules for dtype promotion, which special cases
        # scalars and 0d ndarrays (which it considers equivalent) by using
        # their values to compute the result dtype:
        # https://github.com/numpy/numpy/issues/6240
        # We don't inspect the values of 0d dask arrays, because these could
        # hold potentially very expensive calculations.
        vals = [np.empty((1,) * a.ndim, dtype=a.dtype)
                if not is_scalar_for_elemwise(a) else a
                for a in args]
        try:
            dt = op(*vals).dtype
        except AttributeError:
            dt = None

    name = kwargs.get('name', None) or '%s-%s' % (funcname(op),
                                                  tokenize(op, dt, *args))

    if other:
        return atop(partial_by_order, expr_inds,
                    *concat((a, tuple(range(a.ndim)[::-1])) for a in arrays),
                    dtype=dt, name=name, function=op, other=other,
                    token=funcname(op))
    else:
        return atop(op, expr_inds,
                    *concat((a, tuple(range(a.ndim)[::-1])) for a in arrays),
                    dtype=dt, name=name)
