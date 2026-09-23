def numel(x, **kwargs):
    """ A reduction to count the number of elements """
    return chunk.sum(np.ones_like(x), **kwargs)
