def transposelist(arrays, axes, extradims=0):
    """ Permute axes of nested list

    >>> transposelist([[1,1,1],[1,1,1]], [2,1])
    [[[1, 1], [1, 1], [1, 1]]]

    >>> transposelist([[1,1,1],[1,1,1]], [2,1], extradims=1)
    [[[[1], [1]], [[1], [1]], [[1], [1]]]]
    """
    if len(axes) != ndimlist(arrays):
        raise ValueError("Length of axes should equal depth of nested arrays")
    if extradims < 0:
        raise ValueError("`newdims` should be positive")
    if len(axes) > len(set(axes)):
        raise ValueError("`axes` should be unique")

    ndim = max(axes) + 1
    shape = shapelist(arrays)
    newshape = [shape[axes.index(i)] if i in axes else 1 for i in range(ndim + extradims)]

    result = list(core.flatten(arrays))
    return reshapelist(newshape, result)
