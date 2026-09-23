def compression_level(n, q, oversampling=10, min_subspace_size=20):
    """ Compression level to use in svd_compressed

    Given the size ``n`` of a space, compress that that to one of size
    ``q`` plus oversampling.

    The oversampling allows for greater flexibility in finding an
    appropriate subspace, a low value is often enough (10 is already a
    very conservative choice, it can be further reduced).
    ``q + oversampling`` should not be larger than ``n``.  In this
    specific implementation, ``q + oversampling`` is at least
    ``min_subspace_size``.

    >>> compression_level(100, 10)
    20
    """
    return min(max(min_subspace_size, q + oversampling), n)
