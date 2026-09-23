def arg_combine(func, argfunc, data, axis=None, **kwargs):
    arg, vals = _arg_combine(data, axis, argfunc, keepdims=True)
    result = np.empty(shape=vals.shape, dtype=[('vals', vals.dtype),
                                               ('arg', arg.dtype)])
    result['vals'] = vals
    result['arg'] = arg
    return result
