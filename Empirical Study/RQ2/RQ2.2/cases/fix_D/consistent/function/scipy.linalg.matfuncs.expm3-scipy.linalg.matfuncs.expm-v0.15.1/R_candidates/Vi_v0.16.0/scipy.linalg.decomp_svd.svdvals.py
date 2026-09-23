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

    See also
    --------
    svd : Compute the full singular value decomposition of a matrix.
    diagsvd : Construct the Sigma matrix, given the vector s.

    """
    a = _asarray_validated(a, check_finite=check_finite)
    if a.size:
        return svd(a, compute_uv=0, overwrite_a=overwrite_a,
                check_finite=False)
    elif len(a.shape) != 2:
        raise ValueError('expected matrix')
    else:
        return numpy.empty(0)
