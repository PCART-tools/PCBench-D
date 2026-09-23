def _wrap_masked(f):

    @wraps(f)
    def _(a, value):
        a = asanyarray(a)
        value = asanyarray(value)
        ainds = tuple(range(a.ndim))[::-1]
        vinds = tuple(range(value.ndim))[::-1]
        oinds = max(ainds, vinds, key=len)
        return atop(f, oinds, a, ainds, value, vinds, dtype=a.dtype)

    return _
