def mean_combine(pair, sum=chunk.sum, numel=numel, dtype='f8', **kwargs):
    n = sum(pair['n'], **kwargs)
    total = sum(pair['total'], **kwargs)
    empty = empty_lookup.dispatch(type(n))
    result = empty(n.shape, dtype=pair.dtype)
    result['n'] = n
    result['total'] = total
    return result
