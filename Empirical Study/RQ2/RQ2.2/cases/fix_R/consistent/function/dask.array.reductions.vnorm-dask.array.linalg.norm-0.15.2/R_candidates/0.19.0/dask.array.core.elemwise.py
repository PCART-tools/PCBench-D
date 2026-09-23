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
    out = kwargs.pop('out', None)
    if not set(['name', 'dtype']).issuperset(kwargs):
        msg = "%s does not take the following keyword arguments %s"
        raise TypeError(msg % (op.__name__, str(sorted(set(kwargs) - set(['name', 'dtype'])))))

    args = [np.asarray(a) if isinstance(a, (list, tuple)) else a for a in args]

    shapes = []
    for arg in args:
        shape = getattr(arg, "shape", ())
        if any(is_dask_collection(x) for x in shape):
            # Want to excluded Delayed shapes and dd.Scalar
            shape = ()
        shapes.append(shape)

    shapes = [s if isinstance(s, Iterable) else () for s in shapes]
    out_ndim = len(broadcast_shapes(*shapes))   # Raises ValueError if dimensions mismatch
    expr_inds = tuple(range(out_ndim))[::-1]

    need_enforce_dtype = False
    if 'dtype' in kwargs:
        dt = kwargs['dtype']
    else:
        # We follow NumPy's rules for dtype promotion, which special cases
        # scalars and 0d ndarrays (which it considers equivalent) by using
        # their values to compute the result dtype:
        # https://github.com/numpy/numpy/issues/6240
        # We don't inspect the values of 0d dask arrays, because these could
        # hold potentially very expensive calculations. Instead, we treat
        # them just like other arrays, and if necessary cast the result of op
        # to match.
        vals = [np.empty((1,) * max(1, a.ndim), dtype=a.dtype)
                if not is_scalar_for_elemwise(a) else a
                for a in args]
        try:
            dt = apply_infer_dtype(op, vals, {}, 'elemwise', suggest_dtype=False)
        except Exception:
            return NotImplemented
        need_enforce_dtype = any(not is_scalar_for_elemwise(a) and a.ndim == 0 for a in args)

    name = kwargs.get('name', None) or '%s-%s' % (funcname(op),
                                                  tokenize(op, dt, *args))

    atop_kwargs = dict(dtype=dt, name=name, token=funcname(op).strip('_'))
    if need_enforce_dtype:
        atop_kwargs['enforce_dtype'] = dt
        atop_kwargs['enforce_dtype_function'] = op
        op = _enforce_dtype
    result = atop(op, expr_inds,
                  *concat((a, tuple(range(a.ndim)[::-1])
                           if not is_scalar_for_elemwise(a)
                           else None) for a in args),
                  **atop_kwargs)

    return handle_out(out, result)
