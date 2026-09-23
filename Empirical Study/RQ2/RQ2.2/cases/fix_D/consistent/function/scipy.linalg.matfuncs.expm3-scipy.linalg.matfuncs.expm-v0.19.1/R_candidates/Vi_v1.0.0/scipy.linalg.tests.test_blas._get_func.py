def _get_func(func, ps='sdzc'):
    """Just a helper: return a specified BLAS function w/typecode."""
    for p in ps:
        f = getattr(fblas, p+func, None)
        if f is None:
            continue
        yield f
