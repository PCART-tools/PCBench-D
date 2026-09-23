def is_sparse(array):
    """ return if we are a sparse array """
    return isinstance(array, (gt.ABCSparseArray, gt.ABCSparseSeries))
