def lu(a, permute_l=False, overwrite_a=False, check_finite=True):
    """
    Compute pivoted LU decomposition of a matrix.

    The decomposition is::

        A = P L U

    where P is a permutation matrix, L lower triangular with unit
    diagonal elements, and U upper triangular.

    Parameters
    ----------
    a : (M, N) array_like
        Array to decompose
    permute_l : bool
        Perform the multiplication P*L  (Default: do not permute)
    overwrite_a : bool
        Whether to overwrite data in a (may improve performance)
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    **(If permute_l == False)**

    p : (M, M) ndarray
        Permutation matrix
    l : (M, K) ndarray
        Lower triangular or trapezoidal matrix with unit diagonal.
        K = min(M, N)
    u : (K, N) ndarray
        Upper triangular or trapezoidal matrix

    **(If permute_l == True)**

    pl : (M, K) ndarray
        Permuted L matrix.
        K = min(M, N)
    u : (K, N) ndarray
        Upper triangular or trapezoidal matrix

    Notes
    -----
    This is a LU factorization routine written for Scipy.

    """
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if len(a1.shape) != 2:
        raise ValueError('expected matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    flu, = get_flinalg_funcs(('lu',), (a1,))
    p, l, u, info = flu(a1, permute_l=permute_l, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of '
                                            'internal lu.getrf' % -info)
    if permute_l:
        return l, u
    return p, l, u
