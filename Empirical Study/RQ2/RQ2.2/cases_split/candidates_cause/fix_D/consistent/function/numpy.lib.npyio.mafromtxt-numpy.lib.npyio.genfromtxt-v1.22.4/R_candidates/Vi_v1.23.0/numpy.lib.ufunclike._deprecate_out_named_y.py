def _deprecate_out_named_y(f):
    """
    Allow the out argument to be passed as the name `y` (deprecated)

    In future, this decorator should be removed.
    """
    @functools.wraps(f)
    def func(x, out=None, **kwargs):
        if 'y' in kwargs:
            if 'out' in kwargs:
                raise TypeError(
                    "{} got multiple values for argument 'out'/'y'"
                    .format(f.__name__)
                )
            out = kwargs.pop('y')
            # NumPy 1.13.0, 2017-04-26
            warnings.warn(
                "The name of the out argument to {} has changed from `y` to "
                "`out`, to match other ufuncs.".format(f.__name__),
                DeprecationWarning, stacklevel=3)
        return f(x, out=out, **kwargs)

    return func
