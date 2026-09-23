def arg_agg(func, argfunc, data, axis=None, **kwargs):
    return _arg_combine(data, axis, argfunc, keepdims=False)[0]
