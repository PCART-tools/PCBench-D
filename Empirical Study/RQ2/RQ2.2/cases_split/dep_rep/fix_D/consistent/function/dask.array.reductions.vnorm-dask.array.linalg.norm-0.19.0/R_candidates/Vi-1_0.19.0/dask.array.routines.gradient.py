@wraps(np.gradient)
def gradient(f, *varargs, **kwargs):
    f = asarray(f)

    if not all([isinstance(e, Number) for e in varargs]):
        raise NotImplementedError("Only numeric scalar spacings supported.")

    if varargs == ():
        varargs = (1,)
    if len(varargs) == 1:
        varargs = f.ndim * varargs
    if len(varargs) != f.ndim:
        raise TypeError(
            "Spacing must either be a scalar or a scalar per dimension."
        )

    kwargs["edge_order"] = math.ceil(kwargs.get("edge_order", 1))
    if kwargs["edge_order"] > 2:
        raise ValueError("edge_order must be less than or equal to 2.")

    drop_result_list = False
    axis = kwargs.pop("axis", None)
    if axis is None:
        axis = tuple(range(f.ndim))
    elif isinstance(axis, Integral):
        drop_result_list = True
        axis = (axis,)

    axis = validate_axis(axis, f.ndim)

    if len(axis) != len(set(axis)):
        raise ValueError("duplicate axes not allowed")

    axis = tuple(ax % f.ndim for ax in axis)

    if issubclass(f.dtype.type, (np.bool8, Integral)):
        f = f.astype(float)
    elif issubclass(f.dtype.type, Real) and f.dtype.itemsize < 4:
        f = f.astype(float)

    r = [
        f.map_overlap(
            _gradient_kernel,
            dtype=f.dtype,
            depth={j: 1 if j == ax else 0 for j in range(f.ndim)},
            boundary="none",
            grad_varargs=(varargs[i],),
            grad_kwargs=merge(kwargs, {"axis": ax}),
        )
        for i, ax in enumerate(axis)
    ]
    if drop_result_list:
        r = r[0]

    return r
