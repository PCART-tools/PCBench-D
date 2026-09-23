def mean_chunk(x, sum=chunk.sum, numel=numel, dtype='f8', **kwargs):
    n = numel(x, dtype=dtype, **kwargs)
    total = sum(x, dtype=dtype, **kwargs)
    empty = empty_lookup.dispatch(type(n))
    result = empty(n.shape, dtype=[('total', total.dtype), ('n', n.dtype)])
    result['n'] = n
    result['total'] = total
    return result
