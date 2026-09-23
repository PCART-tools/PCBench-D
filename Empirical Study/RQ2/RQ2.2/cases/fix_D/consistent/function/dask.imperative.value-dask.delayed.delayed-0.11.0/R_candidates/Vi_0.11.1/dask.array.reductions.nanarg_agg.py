def nanarg_agg(func, argfunc, data, axis=None, **kwargs):
    arg, vals = _arg_combine(data, axis, argfunc, keepdims=False)
    if np.any(np.isnan(vals)):
        raise ValueError("All NaN slice encountered")
    return arg
