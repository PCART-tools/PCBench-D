def vnorm(a, ord=None, axis=None, dtype=None, keepdims=False, split_every=None,
          out=None):
    """ Vector norm

    See np.linalg.norm
    """
    if ord is None or ord == 'fro':
        ord = 2
    if ord == np.inf:
        return max(abs(a), axis=axis, keepdims=keepdims,
                   split_every=split_every, out=out)
    elif ord == -np.inf:
        return min(abs(a), axis=axis, keepdims=keepdims,
                   split_every=split_every, out=out)
    elif ord == 1:
        return sum(abs(a), axis=axis, dtype=dtype, keepdims=keepdims,
                   split_every=split_every, out=out)
    else:
        return sum(abs(a) ** ord, axis=axis, dtype=dtype, keepdims=keepdims,
                   split_every=split_every, out=out) ** (1. / ord)
