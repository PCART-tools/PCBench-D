def ghost(x, depth, boundary):
    """ Share boundaries between neighboring blocks

    Parameters
    ----------

    x: da.Array
        A dask array
    depth: dict
        The size of the shared boundary per axis
    boundary: dict
        The boundary condition on each axis. Options are 'reflect', 'periodic',
        'nearest', 'none', an integer will fill the boundary with that integer.

    The axes dict informs how many cells to overlap between neighboring blocks
    {0: 2, 2: 5} means share two cells in 0 axis, 5 cells in 2 axis

    Examples
    --------

    >>> import numpy as np
    >>> import dask.array as da

    >>> x = np.arange(64).reshape((8, 8))
    >>> d = da.from_array(x, chunks=(4, 4))
    >>> d.chunks
    ((4, 4), (4, 4))

    >>> g = da.ghost.ghost(d, depth={0: 2, 1: 1},
    ...                       boundary={0: 100, 1: 'reflect'})
    >>> g.chunks
    ((8, 8), (6, 6))

    >>> np.array(g)
    array([[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
           [  0,   0,   1,   2,   3,   4,   3,   4,   5,   6,   7,   7],
           [  8,   8,   9,  10,  11,  12,  11,  12,  13,  14,  15,  15],
           [ 16,  16,  17,  18,  19,  20,  19,  20,  21,  22,  23,  23],
           [ 24,  24,  25,  26,  27,  28,  27,  28,  29,  30,  31,  31],
           [ 32,  32,  33,  34,  35,  36,  35,  36,  37,  38,  39,  39],
           [ 40,  40,  41,  42,  43,  44,  43,  44,  45,  46,  47,  47],
           [ 16,  16,  17,  18,  19,  20,  19,  20,  21,  22,  23,  23],
           [ 24,  24,  25,  26,  27,  28,  27,  28,  29,  30,  31,  31],
           [ 32,  32,  33,  34,  35,  36,  35,  36,  37,  38,  39,  39],
           [ 40,  40,  41,  42,  43,  44,  43,  44,  45,  46,  47,  47],
           [ 48,  48,  49,  50,  51,  52,  51,  52,  53,  54,  55,  55],
           [ 56,  56,  57,  58,  59,  60,  59,  60,  61,  62,  63,  63],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]])
    """
    depth2 = coerce_depth(x.ndim, depth)
    boundary2 = coerce_boundary(x.ndim, boundary)

    # is depth larger than chunk size?
    depth_values = [depth2.get(i, 0) for i in range(x.ndim)]
    for d, c in zip(depth_values, x.chunks):
        if d > min(c):
            raise ValueError("The overlapping depth %d is larger than your\n"
                             "smallest chunk size %d. Rechunk your array\n"
                             "with a larger chunk size or a chunk size that\n"
                             "more evenly divides the shape of your array." %
                             (d, min(c)))
    x2 = boundaries(x, depth2, boundary2)
    x3 = ghost_internal(x2, depth2)
    trim = dict((k, v*2 if boundary2.get(k, 'none') != 'none' else 0)
                for k, v in depth2.items())
    x4 = chunk.trim(x3, trim)
    return x4
