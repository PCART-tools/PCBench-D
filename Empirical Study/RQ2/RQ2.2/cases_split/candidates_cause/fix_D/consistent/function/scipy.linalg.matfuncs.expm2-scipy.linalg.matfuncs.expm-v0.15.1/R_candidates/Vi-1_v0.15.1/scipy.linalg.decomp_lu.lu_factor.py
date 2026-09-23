def lu_factor(a, overwrite_a=False, check_finite=True):
    """
    Compute pivoted LU decomposition of a matrix.

    The decomposition is::

        A = P L U

    where P is a permutation matrix, L lower triangular with unit
    diagonal elements, and U upper triangular.

    Parameters
    ----------
    a : (M, M) array_like
        Matrix to decompose
    overwrite_a : boolean
        Whether to overwrite data in A (may increase performance)
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    lu : (N, N) ndarray
        Matrix containing U in its upper triangle, and L in its lower triangle.
        The unit diagonal elements of L are not stored.
    piv : (N,) ndarray
        Pivot indices representing the permutation matrix P:
        row i of matrix was interchanged with row piv[i].

    See also
    --------
    lu_solve : solve an equation system using the LU factorization of a matrix

    Notes
    -----
    This is a wrapper to the ``*GETRF`` routines from LAPACK.

    """
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if len(a1.shape) != 2 or (a1.shape[0] != a1.shape[1]):
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or (_datacopied(a1, a))
    getrf, = get_lapack_funcs(('getrf',), (a1,))
    lu, piv, info = getrf(a1, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of '
                                'internal getrf (lu_factor)' % -info)
    if info > 0:
        warn("Diagonal number %d is exactly zero. Singular matrix." % info,
                    RuntimeWarning)
    return lu, piv
