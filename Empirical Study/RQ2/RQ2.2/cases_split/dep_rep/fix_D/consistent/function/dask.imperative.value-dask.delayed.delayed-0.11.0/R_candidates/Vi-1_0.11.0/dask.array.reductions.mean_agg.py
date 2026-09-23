def mean_agg(pair, dtype='f8', **kwargs):
    return divide(pair['total'].sum(dtype=dtype, **kwargs),
                  pair['n'].sum(dtype=dtype, **kwargs), dtype=dtype)
