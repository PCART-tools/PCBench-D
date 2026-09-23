def solve_triangular(a, b, trans=0, lower=False, unit_diagonal=False,
                     overwrite_b=False, debug=False, check_finite=True):
    """
    Solve the equation `a x = b` for `x`, assuming a is a triangular matrix.

    Parameters
    ----------
    a : (M, M) array_like
        A triangular matrix
    b : (M,) or (M, N) array_like
        Right-hand side matrix in `a x = b`
    lower : boolean
        Use only data contained in the lower triangle of `a`.
        Default is to use upper triangle.
    trans : {0, 1, 2, 'N', 'T', 'C'}, optional
        Type of system to solve:

        ========  =========
        trans     system
        ========  =========
        0 or 'N'  a x  = b
        1 or 'T'  a^T x = b
        2 or 'C'  a^H x = b
        ========  =========
    unit_diagonal : bool, optional
        If True, diagonal elements of `a` are assumed to be 1 and
        will not be referenced.
    overwrite_b : bool, optional
        Allow overwriting data in `b` (may enhance performance)
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, N) ndarray
        Solution to the system `a x = b`.  Shape of return matches `b`.

    Raises
    ------
    LinAlgError
        If `a` is singular

    Notes
    -----
    .. versionadded:: 0.9.0

    """

    if check_finite:
        a1, b1 = map(np.asarray_chkfinite,(a,b))
    else:
        a1, b1 = map(np.asarray, (a,b))
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')
    if a1.shape[0] != b1.shape[0]:
        raise ValueError('incompatible dimensions')
    overwrite_b = overwrite_b or _datacopied(b1, b)
    if debug:
        print('solve:overwrite_b=',overwrite_b)
    trans = {'N': 0, 'T': 1, 'C': 2}.get(trans, trans)
    trtrs, = get_lapack_funcs(('trtrs',), (a1,b1))
    x, info = trtrs(a1, b1, overwrite_b=overwrite_b, lower=lower,
                    trans=trans, unitdiag=unit_diagonal)

    if info == 0:
        return x
    if info > 0:
        raise LinAlgError("singular matrix: resolution failed at diagonal %s" % (info-1))
    raise ValueError('illegal value in %d-th argument of internal trtrs'
            % -info)
