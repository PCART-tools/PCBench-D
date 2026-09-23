def svdvals(a, overwrite_a=False, check_finite=True):
    """
    Compute singular values of a matrix.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to decompose.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance.
        Default is False.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    s : (min(M, N),) ndarray
        The singular values, sorted in decreasing order.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    Notes
    -----
    ``svdvals(a)`` only differs from ``svd(a, compute_uv=False)`` by its
    handling of the edge case of empty ``a``, where it returns an
    empty sequence:

    >>> a = np.empty((0, 2))
    >>> from scipy.linalg import svdvals
    >>> svdvals(a)
    array([], dtype=float64)

    See Also
    --------
    svd : Compute the full singular value decomposition of a matrix.
    diagsvd : Construct the Sigma matrix, given the vector s.

    Examples
    --------
    >>> from scipy.linalg import svdvals
    >>> m = np.array([[1.0, 0.0],
    ...               [2.0, 3.0],
    ...               [1.0, 1.0],
    ...               [0.0, 2.0],
    ...               [1.0, 0.0]])
    >>> svdvals(m)
    array([ 4.28091555,  1.63516424])

    We can verify the maximum singular value of `m` by computing the maximum
    length of `m.dot(u)` over all the unit vectors `u` in the (x,y) plane.
    We approximate "all" the unit vectors with a large sample.  Because
    of linearity, we only need the unit vectors with angles in [0, pi].

    >>> t = np.linspace(0, np.pi, 2000)
    >>> u = np.array([np.cos(t), np.sin(t)])
    >>> np.linalg.norm(m.dot(u), axis=0).max()
    4.2809152422538475

    `p` is a projection matrix with rank 1.  With exact arithmetic,
    its singular values would be [1, 0, 0, 0].

    >>> v = np.array([0.1, 0.3, 0.9, 0.3])
    >>> p = np.outer(v, v)
    >>> svdvals(p)
    array([  1.00000000e+00,   2.02021698e-17,   1.56692500e-17,
             8.15115104e-34])

    The singular values of an orthogonal matrix are all 1.  Here we
    create a random orthogonal matrix by using the `rvs()` method of
    `scipy.stats.ortho_group`.

    >>> from scipy.stats import ortho_group
    >>> np.random.seed(123)
    >>> orth = ortho_group.rvs(4)
    >>> svdvals(orth)
    array([ 1.,  1.,  1.,  1.])

    """
    a = _asarray_validated(a, check_finite=check_finite)
    if a.size:
        return svd(a, compute_uv=0, overwrite_a=overwrite_a,
                   check_finite=False)
    elif len(a.shape) != 2:
        raise ValueError('expected matrix')
    else:
        return numpy.empty(0)
