def solve(a, b, sym_pos=False, lower=False, overwrite_a=False, overwrite_b=False,
          debug=False, check_finite=True):
    """
    Solve the equation ``a x = b`` for ``x``.

    Parameters
    ----------
    a : (M, M) array_like
        A square matrix.
    b : (M,) or (M, N) array_like
        Right-hand side matrix in ``a x = b``.
    sym_pos : bool
        Assume `a` is symmetric and positive definite.
    lower : boolean
        Use only data contained in the lower triangle of `a`, if `sym_pos` is
        true.  Default is to use upper triangle.
    overwrite_a : bool
        Allow overwriting data in `a` (may enhance performance).
        Default is False.
    overwrite_b : bool
        Allow overwriting data in `b` (may enhance performance).
        Default is False.
    check_finite : boolean, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, N) ndarray
        Solution to the system ``a x = b``.  Shape of the return matches the
        shape of `b`.

    Raises
    ------
    LinAlgError
        If `a` is singular.

    Examples
    --------
    Given `a` and `b`, solve for `x`:

    >>> a = np.array([[3,2,0],[1,-1,0],[0,5,1]])
    >>> b = np.array([2,4,-1])
    >>> x = linalg.solve(a,b)
    >>> x
    array([ 2., -2.,  9.])
    >>> np.dot(a, x) == b
    array([ True,  True,  True], dtype=bool)

    """
    if check_finite:
        a1, b1 = map(np.asarray_chkfinite,(a,b))
    else:
        a1, b1 = map(np.asarray, (a,b))
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')
    if a1.shape[0] != b1.shape[0]:
        raise ValueError('incompatible dimensions')
    overwrite_a = overwrite_a or _datacopied(a1, a)
    overwrite_b = overwrite_b or _datacopied(b1, b)
    if debug:
        print('solve:overwrite_a=',overwrite_a)
        print('solve:overwrite_b=',overwrite_b)
    if sym_pos:
        posv, = get_lapack_funcs(('posv',), (a1,b1))
        c, x, info = posv(a1, b1, lower=lower,
                        overwrite_a=overwrite_a,
                        overwrite_b=overwrite_b)
    else:
        gesv, = get_lapack_funcs(('gesv',), (a1,b1))
        lu, piv, x, info = gesv(a1, b1, overwrite_a=overwrite_a,
                                            overwrite_b=overwrite_b)

    if info == 0:
        return x
    if info > 0:
        raise LinAlgError("singular matrix")
    raise ValueError('illegal value in %d-th argument of internal gesv|posv'
                                                                    % -info)
