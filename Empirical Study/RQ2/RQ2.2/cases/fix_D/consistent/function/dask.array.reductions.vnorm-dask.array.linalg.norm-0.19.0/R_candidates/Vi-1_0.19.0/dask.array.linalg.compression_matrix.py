def compression_matrix(data, q, n_power_iter=0, seed=None):
    """ Randomly sample matrix to find most active subspace

    This compression matrix returned by this algorithm can be used to
    compute both the QR decomposition and the Singular Value
    Decomposition.

    Parameters
    ----------
    data: Array
    q: int
        Size of the desired subspace (the actual size will be bigger,
        because of oversampling, see ``da.linalg.compression_level``)
    n_power_iter: int
        number of power iterations, useful when the singular values of
        the input matrix decay very slowly.

    References
    ----------
    N. Halko, P. G. Martinsson, and J. A. Tropp.
    Finding structure with randomness: Probabilistic algorithms for
    constructing approximate matrix decompositions.
    SIAM Rev., Survey and Review section, Vol. 53, num. 2,
    pp. 217-288, June 2011
    http://arxiv.org/abs/0909.4061
    """
    n = data.shape[1]
    comp_level = compression_level(n, q)
    state = RandomState(seed)
    omega = state.standard_normal(size=(n, comp_level), chunks=(data.chunks[1],
                                                                (comp_level,)))
    mat_h = data.dot(omega)
    for j in range(n_power_iter):
        mat_h = data.dot(data.T.dot(mat_h))
    q, _ = tsqr(mat_h)
    return q.T
