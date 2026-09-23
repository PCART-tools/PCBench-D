def is_nested_tuple(tup, labels):
    # check for a compatiable nested tuple and multiindexes among the axes
    if not isinstance(tup, tuple):
        return False

    # are we nested tuple of: tuple,list,slice
    for i, k in enumerate(tup):

        if isinstance(k, (tuple, list, slice)):
            return isinstance(labels, MultiIndex)

    return False
