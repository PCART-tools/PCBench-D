def topk(k, x):
    """ Top k elements of an array

    >>> topk(2, np.array([5, 1, 3, 6]))
    array([6, 5])
    """
    # http://stackoverflow.com/a/23734295/616616 by larsmans
    k = np.minimum(k, len(x))
    ind = np.argpartition(x, -k)[-k:]
    return np.sort(x[ind])[::-1]
