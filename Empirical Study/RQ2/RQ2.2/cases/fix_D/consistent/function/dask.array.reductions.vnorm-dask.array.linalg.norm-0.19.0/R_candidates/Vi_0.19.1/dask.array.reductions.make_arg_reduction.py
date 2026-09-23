def make_arg_reduction(func, argfunc, is_nan_func=False):
    """ Create an argreduction callable

    Parameters
    ----------
    func : callable
        The reduction (e.g. ``min``)
    argfunc : callable
        The argreduction (e.g. ``argmin``)
    """
    chunk = partial(arg_chunk, func, argfunc)
    combine = partial(arg_combine, func, argfunc)
    if is_nan_func:
        agg = partial(nanarg_agg, func, argfunc)
    else:
        agg = partial(arg_agg, func, argfunc)

    @wraps(argfunc)
    def _(x, axis=None, split_every=None, out=None):
        return arg_reduction(x, chunk, combine, agg, axis,
                             split_every=split_every, out=out)

    return _
