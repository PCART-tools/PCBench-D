def new_blockdim(dim_shape, lengths, index):
    """

    >>> new_blockdim(100, [20, 10, 20, 10, 40], slice(0, 90, 2))
    [10, 5, 10, 5, 15]

    >>> new_blockdim(100, [20, 10, 20, 10, 40], [5, 1, 30, 22])
    [4]

    >>> new_blockdim(100, [20, 10, 20, 10, 40], slice(90, 10, -2))
    [16, 5, 10, 5, 4]
    """
    if index == slice(None, None, None):
        return lengths
    if isinstance(index, list):
        return [len(index)]
    assert not isinstance(index, Integral)
    pairs = sorted(_slice_1d(dim_shape, lengths, index).items(),
                   key=itemgetter(0))
    slices = [slice(0, lengths[i], 1) if slc == slice(None, None, None) else slc
              for i, slc in pairs]
    if isinstance(index, slice) and index.step and index.step < 0:
        slices = slices[::-1]
    return [int(math.ceil((1. * slc.stop - slc.start) / slc.step)) for slc in slices]
