def arg_chunk(func, argfunc, x, axis, offset_info):
    arg_axis = None if len(axis) == x.ndim or x.ndim == 1 else axis[0]
    vals = func(x, axis=arg_axis, keepdims=True)
    arg = argfunc(x, axis=arg_axis, keepdims=True)
    if arg_axis is None:
        offset, total_shape = offset_info
        ind = np.unravel_index(arg.ravel()[0], x.shape)
        total_ind = tuple(o + i for (o, i) in zip(offset, ind))
        arg[:] = np.ravel_multi_index(total_ind, total_shape)
    else:
        arg += offset_info

    if isinstance(vals, np.ma.masked_array):
        if 'min' in argfunc.__name__:
            fill_value = np.ma.minimum_fill_value(vals)
        else:
            fill_value = np.ma.maximum_fill_value(vals)
        vals = np.ma.filled(vals, fill_value)

    result = np.empty(shape=vals.shape, dtype=[('vals', vals.dtype),
                                               ('arg', arg.dtype)])
    result['vals'] = vals
    result['arg'] = arg
    return result
