def moment_chunk(A, order=2, sum=chunk.sum, numel=numel, dtype='f8', **kwargs):
    total = sum(A, dtype=dtype, **kwargs)
    n = numel(A, **kwargs)
    u = total / n
    M = np.empty(shape=n.shape + (order - 1,), dtype=dtype)
    for i in range(2, order + 1):
        M[..., i - 2] = sum((A - u)**i, dtype=dtype, **kwargs)
    result = np.empty(shape=n.shape, dtype=[('total', total.dtype),
                                            ('n', n.dtype),
                                            ('M', M.dtype, (order - 1,))])
    result['total'] = total
    result['n'] = n
    result['M'] = M
    return result
