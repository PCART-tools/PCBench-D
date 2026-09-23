def lu_solve(lu_and_piv, b, trans=0, overwrite_b=False, check_finite=True):
    """Solve an equation system, a x = b, given the LU factorization of a

    Parameters
    ----------
    (lu, piv)
        Factorization of the coefficient matrix a, as given by lu_factor
    b : array
        Right-hand side
    trans : {0, 1, 2}, optional
        Type of system to solve:

        =====  =========
        trans  system
        =====  =========
        0      a x   = b
        1      a^T x = b
        2      a^H x = b
        =====  =========
    overwrite_b : bool, optional
        Whether to overwrite data in b (may increase performance)
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : array
        Solution to the system

    See also
    --------
    lu_factor : LU factorize a matrix

    """
    (lu, piv) = lu_and_piv
    if check_finite:
        b1 = asarray_chkfinite(b)
    else:
        b1 = asarray(b)
    overwrite_b = overwrite_b or _datacopied(b1, b)
    if lu.shape[0] != b1.shape[0]:
        raise ValueError("incompatible dimensions.")

    getrs, = get_lapack_funcs(('getrs',), (lu, b1))
    x,info = getrs(lu, piv, b1, trans=trans, overwrite_b=overwrite_b)
    if info == 0:
        return x
    raise ValueError('illegal value in %d-th argument of internal gesv|posv'
                                                                    % -info)
