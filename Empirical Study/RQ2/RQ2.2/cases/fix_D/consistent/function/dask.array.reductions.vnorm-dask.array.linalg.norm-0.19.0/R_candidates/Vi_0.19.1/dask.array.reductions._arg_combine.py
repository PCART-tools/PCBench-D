def _arg_combine(data, axis, argfunc, keepdims=False):
    """ Merge intermediate results from ``arg_*`` functions"""
    axis = None if len(axis) == data.ndim or data.ndim == 1 else axis[0]
    vals = data['vals']
    arg = data['arg']
    if axis is None:
        local_args = argfunc(vals, axis=axis, keepdims=keepdims)
        vals = vals.ravel()[local_args]
        arg = arg.ravel()[local_args]
    else:
        local_args = argfunc(vals, axis=axis)
        inds = np.ogrid[tuple(map(slice, local_args.shape))]
        inds.insert(axis, local_args)
        inds = tuple(inds)
        vals = vals[inds]
        arg = arg[inds]
        if keepdims:
            vals = np.expand_dims(vals, axis)
            arg = np.expand_dims(arg, axis)
    return arg, vals
