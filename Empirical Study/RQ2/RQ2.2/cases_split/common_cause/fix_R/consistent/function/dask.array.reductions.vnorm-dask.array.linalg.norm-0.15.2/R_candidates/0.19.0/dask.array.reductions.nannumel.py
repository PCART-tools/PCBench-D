def nannumel(x, **kwargs):
    """ A reduction to count the number of elements """
    return chunk.sum(~np.isnan(x), **kwargs)
