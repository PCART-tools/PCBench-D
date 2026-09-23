def moment_agg(data, order=2, ddof=0, dtype='f8', sum=np.sum, **kwargs):
    totals = data['total']
    ns = data['n']
    Ms = data['M']

    kwargs['dtype'] = dtype
    # To properly handle ndarrays, the original dimensions need to be kept for
    # part of the calculation.
    keepdim_kw = kwargs.copy()
    keepdim_kw['keepdims'] = True

    n = sum(ns, **keepdim_kw)
    mu = divide(totals.sum(**keepdim_kw), n, dtype=dtype)
    inner_term = divide(totals, ns, dtype=dtype) - mu

    M = _moment_helper(Ms, ns, inner_term, order, sum, kwargs)
    return divide(M, sum(n, **kwargs) - ddof, dtype=dtype)
