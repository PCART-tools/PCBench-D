def moment_combine(data, order=2, ddof=0, dtype='f8', sum=np.sum, **kwargs):
    kwargs['dtype'] = dtype
    kwargs['keepdims'] = True

    totals = data['total']
    ns = data['n']
    Ms = data['M']
    total = totals.sum(**kwargs)
    n = sum(ns, **kwargs)
    mu = divide(total, n, dtype=dtype)
    inner_term = divide(totals, ns, dtype=dtype) - mu
    M = np.empty(shape=n.shape + (order - 1,), dtype=dtype)

    for o in range(2, order + 1):
        M[..., o - 2] = _moment_helper(Ms, ns, inner_term, o, sum, kwargs)

    result = np.zeros(shape=n.shape, dtype=[('total', total.dtype),
                                            ('n', n.dtype),
                                            ('M', Ms.dtype, (order-1,))])
    result['total'] = total
    result['n'] = n
    result['M'] = M
    return result
