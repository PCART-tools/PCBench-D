def unify_chunks(*args):
    """ Unify chunks across a sequence of arrays

    Currently only uses very simple rules for unifying chunks: see
    common_blockdim for more details.

    Parameters
    ----------
    *args: sequence of Array, index pairs
        Sequence like (x, 'ij', y, 'jk', z, 'i')

    Returns
    -------
    chunkss : dict
        Map like {index: chunks}.
    arrays : list
        List of rechunked arrays.
    """
    arginds = list(partition(2, args)) # [x, ij, y, jk] -> [(x, ij), (y, jk)]

    nameinds = [(a.name, i) for a, i in arginds]
    blockdim_dict = dict((a.name, a.chunks) for a, _ in arginds)

    chunkss = broadcast_dimensions(nameinds, blockdim_dict,
                                   consolidate=common_blockdim)
    arrays = [a.rechunk(tuple(chunkss[j] if a.shape[n] > 1 else 1
                              for n, j in enumerate(i)))
              for a, i in arginds]
    return chunkss, arrays
