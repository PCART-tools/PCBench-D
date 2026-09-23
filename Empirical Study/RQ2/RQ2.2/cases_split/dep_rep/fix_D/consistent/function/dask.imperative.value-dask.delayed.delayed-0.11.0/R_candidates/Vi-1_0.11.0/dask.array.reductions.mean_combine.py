def mean_combine(pair, sum=chunk.sum, numel=numel, dtype='f8', **kwargs):
    n = sum(pair['n'], **kwargs)
    total = sum(pair['total'], **kwargs)
    result = np.empty(shape=n.shape, dtype=pair.dtype)
    result['n'] = n
    result['total'] = total
    return result
