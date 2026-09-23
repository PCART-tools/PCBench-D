def _fix_out_named_y(f):
    """
    Allow the out argument to be passed as the name `y` (deprecated)

    This decorator should only be used if _deprecate_out_named_y is used on
    a corresponding dispatcher function.
    """
    @functools.wraps(f)
    def func(x, out=None, **kwargs):
        if 'y' in kwargs:
            # we already did error checking in _deprecate_out_named_y
            out = kwargs.pop('y')
        return f(x, out=out, **kwargs)

    return func
