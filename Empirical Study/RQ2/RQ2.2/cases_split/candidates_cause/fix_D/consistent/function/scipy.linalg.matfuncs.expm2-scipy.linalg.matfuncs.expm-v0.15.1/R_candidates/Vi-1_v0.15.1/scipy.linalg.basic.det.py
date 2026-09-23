def det(a, overwrite_a=False, check_finite=True):
    """
    Compute the determinant of a matrix

    The determinant of a square matrix is a value derived arithmetically
    from the coefficients of the matrix.

    The determinant for a 3x3 matrix, for example, is computed as follows::

        a    b    c
        d    e    f = A
        g    h    i

        det(A) = a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h

    Parameters
    ----------
    a : (M, M) array_like
        A square matrix.
    overwrite_a : bool
        Allow overwriting data in a (may enhance performance).
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    det : float or complex
        Determinant of `a`.

    Notes
    -----
    The determinant is computed via LU factorization, LAPACK routine z/dgetrf.

    Examples
    --------
    >>> a = np.array([[1,2,3],[4,5,6],[7,8,9]])
    >>> linalg.det(a)
    0.0
    >>> a = np.array([[0,2,3],[4,5,6],[7,8,9]])
    >>> linalg.det(a)
    3.0

    """
    if check_finite:
        a1 = np.asarray_chkfinite(a)
    else:
        a1 = np.asarray(a)
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or _datacopied(a1, a)
    fdet, = get_flinalg_funcs(('det',), (a1,))
    a_det, info = fdet(a1, overwrite_a=overwrite_a)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal '
                                                        'det.getrf' % -info)
    return a_det
