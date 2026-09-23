def _enforce_dtype(*args, **kwargs):
    """Calls a function and converts its result to the given dtype.

    The parameters have deliberately been given unwieldy names to avoid
    clashes with keyword arguments consumed by atop

    A dtype of `object` is treated as a special case and not enforced,
    because it is used as a dummy value in some places when the result will
    not be a block in an Array.

    Parameters
    ----------
    enforce_dtype : dtype
        Result dtype
    enforce_dtype_function : callable
        The wrapped function, which will be passed the remaining arguments
    """
    dtype = kwargs.pop('enforce_dtype')
    function = kwargs.pop('enforce_dtype_function')

    result = function(*args, **kwargs)
    if dtype != result.dtype and dtype != object:
        if not np.can_cast(result, dtype, casting='same_kind'):
            raise ValueError("Inferred dtype from function %r was %r "
                             "but got %r, which can't be cast using "
                             "casting='same_kind'" %
                             (funcname(function), str(dtype), str(result.dtype)))
        if np.isscalar(result):
            # scalar astype method doesn't take the keyword arguments, so
            # have to convert via 0-dimensional array and back.
            result = result.astype(dtype)
        else:
            try:
                result = result.astype(dtype, copy=False)
            except TypeError:
                # Missing copy kwarg
                result = result.astype(dtype)
    return result
