def wrap_func_shape_as_first_arg(func, *args, **kwargs):
    """
    Transform np creation function into blocked version
    """
    if 'shape' not in kwargs:
        shape, args = args[0], args[1:]
    else:
        shape = kwargs.pop('shape')

    if isinstance(shape, np.ndarray):
        shape = shape.tolist()

    if not isinstance(shape, (tuple, list)):
        shape = (shape,)

    chunks = kwargs.pop('chunks', None)

    dtype = kwargs.pop('dtype', None)
    if dtype is None:
        dtype = func(shape, *args, **kwargs).dtype
    dtype = np.dtype(dtype)

    chunks = normalize_chunks(chunks, shape, dtype=dtype)
    name = kwargs.pop('name', None)

    name = name or funcname(func) + '-' + tokenize(func, shape, chunks, dtype, args, kwargs)

    keys = product([name], *[range(len(bd)) for bd in chunks])
    shapes = product(*chunks)
    func = partial(func, dtype=dtype, **kwargs)
    vals = ((func,) + (s,) + args for s in shapes)

    dsk = dict(zip(keys, vals))
    return Array(dsk, name, chunks, dtype=dtype)
