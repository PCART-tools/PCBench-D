def svd_compressed(a, k, n_power_iter=0, seed=None):
    """ Randomly compressed rank-k thin Singular Value Decomposition.

    This computes the approximate singular value decomposition of a large
    array.  This algorithm is generally faster than the normal algorithm
    but does not provide exact results.  One can balance between
    performance and accuracy with input parameters (see below).

    Parameters
    ----------
    a: Array
        Input array
    k: int
        Rank of the desired thin SVD decomposition.
    n_power_iter: int
        Number of power iterations, useful when the singular values
        decay slowly. Error decreases exponentially as n_power_iter
        increases. In practice, set n_power_iter <= 4.

    Examples
    --------

    >>> u, s, vt = svd_compressed(x, 20)  # doctest: +SKIP

    Returns
    -------
    u:  Array, unitary / orthogonal
    s:  Array, singular values in decreasing order (largest first)
    v:  Array, unitary / orthogonal

    References
    ----------
    N. Halko, P. G. Martinsson, and J. A. Tropp.
    Finding structure with randomness: Probabilistic algorithms for
    constructing approximate matrix decompositions.
    SIAM Rev., Survey and Review section, Vol. 53, num. 2,
    pp. 217-288, June 2011
    http://arxiv.org/abs/0909.4061
    """
    comp = compression_matrix(a, k, n_power_iter=n_power_iter, seed=seed)
    a_compressed = comp.dot(a)
    v, s, u = tsqr(a_compressed.T, compute_svd=True)
    u = comp.T.dot(u)
    v = v.T
    u = u[:, :k]
    s = s[:k]
    v = v[:k, :]
    return u, s, v
