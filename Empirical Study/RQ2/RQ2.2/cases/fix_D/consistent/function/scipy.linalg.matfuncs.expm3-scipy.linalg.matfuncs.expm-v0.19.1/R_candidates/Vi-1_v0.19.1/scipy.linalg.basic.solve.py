def solve(a, b, sym_pos=False, lower=False, overwrite_a=False,
          overwrite_b=False, debug=None, check_finite=True, assume_a='gen',
          transposed=False):
    """
    Solves the linear equation set ``a * x = b`` for the unknown ``x``
    for square ``a`` matrix.

    If the data matrix is known to be a particular type then supplying the
    corresponding string to ``assume_a`` key chooses the dedicated solver.
    The available options are

    ===================  ========
     generic matrix       'gen'
     symmetric            'sym'
     hermitian            'her'
     positive definite    'pos'
    ===================  ========

    If omitted, ``'gen'`` is the default structure.

    The datatype of the arrays define which solver is called regardless
    of the values. In other words, even when the complex array entries have
    precisely zero imaginary parts, the complex solver will be called based
    on the data type of the array.

    Parameters
    ----------
    a : (N, N) array_like
        Square input data
    b : (N, NRHS) array_like
        Input data for the right hand side.
    sym_pos : bool, optional
        Assume `a` is symmetric and positive definite. This key is deprecated
        and assume_a = 'pos' keyword is recommended instead. The functionality
        is the same. It will be removed in the future.
    lower : bool, optional
        If True, only the data contained in the lower triangle of `a`. Default
        is to use upper triangle. (ignored for ``'gen'``)
    overwrite_a : bool, optional
        Allow overwriting data in `a` (may enhance performance).
        Default is False.
    overwrite_b : bool, optional
        Allow overwriting data in `b` (may enhance performance).
        Default is False.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    assume_a : str, optional
        Valid entries are explained above.
    transposed: bool, optional
        If True, depending on the data type ``a^T x = b`` or ``a^H x = b`` is
        solved (only taken into account for ``'gen'``).

    Returns
    -------
    x : (N, NRHS) ndarray
        The solution array.

    Raises
    ------
    ValueError
        If size mismatches detected or input a is not square.
    LinAlgError
        If the matrix is singular.
    RuntimeWarning
        If an ill-conditioned input a is detected.

    Examples
    --------
    Given `a` and `b`, solve for `x`:

    >>> a = np.array([[3, 2, 0], [1, -1, 0], [0, 5, 1]])
    >>> b = np.array([2, 4, -1])
    >>> from scipy import linalg
    >>> x = linalg.solve(a, b)
    >>> x
    array([ 2., -2.,  9.])
    >>> np.dot(a, x) == b
    array([ True,  True,  True], dtype=bool)

    Notes
    -----
    If the input b matrix is a 1D array with N elements, when supplied
    together with an NxN input a, it is assumed as a valid column vector
    despite the apparent size mismatch. This is compatible with the
    numpy.dot() behavior and the returned result is still 1D array.

    The generic, symmetric, hermitian and positive definite solutions are
    obtained via calling ?GESVX, ?SYSVX, ?HESVX, and ?POSVX routines of
    LAPACK respectively.
    """
    # Flags for 1D or nD right hand side
    b_is_1D = False
    b_is_ND = False

    a1 = atleast_2d(_asarray_validated(a, check_finite=check_finite))
    b1 = atleast_1d(_asarray_validated(b, check_finite=check_finite))
    n = a1.shape[0]

    overwrite_a = overwrite_a or _datacopied(a1, a)
    overwrite_b = overwrite_b or _datacopied(b1, b)

    if a1.shape[0] != a1.shape[1]:
        raise ValueError('Input a needs to be a square matrix.')

    if n != b1.shape[0]:
        # Last chance to catch 1x1 scalar a and 1D b arrays
        if not (n == 1 and b1.size != 0):
            raise ValueError('Input b has to have same number of rows as '
                             'input a')

    # accomodate empty arrays
    if b1.size == 0:
        return np.asfortranarray(b1.copy())

    # regularize 1D b arrays to 2D and catch nD RHS arrays
    if b1.ndim == 1:
        if n == 1:
            b1 = b1[None, :]
        else:
            b1 = b1[:, None]
        b_is_1D = True
    elif b1.ndim > 2:
        b_is_ND = True

    r_or_c = complex if np.iscomplexobj(a1) else float

    if assume_a in ('gen', 'sym', 'her', 'pos'):
        _structure = assume_a
    else:
        raise ValueError('{} is not a recognized matrix structure'
                         ''.format(assume_a))

    # Deprecate keyword "debug"
    if debug is not None:
        warnings.warn('Use of the "debug" keyword is deprecated '
                      'and this keyword will be removed in the future '
                      'versions of SciPy.', DeprecationWarning)

    # Backwards compatibility - old keyword.
    if sym_pos:
        assume_a = 'pos'

    if _structure == 'gen':
        gesvx = get_lapack_funcs('gesvx', (a1, b1))
        trans_conj = 'N'
        if transposed:
            trans_conj = 'T' if r_or_c is float else 'H'
        (_, _, _, _, _, _, _,
         x, rcond, _, _, info) = gesvx(a1, b1,
                                       trans=trans_conj,
                                       overwrite_a=overwrite_a,
                                       overwrite_b=overwrite_b
                                       )
    elif _structure == 'sym':
        sysvx, sysvx_lw = get_lapack_funcs(('sysvx', 'sysvx_lwork'), (a1, b1))
        lwork = _compute_lwork(sysvx_lw, n, lower)
        _, _, _, _, x, rcond, _, _, info = sysvx(a1, b1, lwork=lwork,
                                                 lower=lower,
                                                 overwrite_a=overwrite_a,
                                                 overwrite_b=overwrite_b
                                                 )
    elif _structure == 'her':
        hesvx, hesvx_lw = get_lapack_funcs(('hesvx', 'hesvx_lwork'), (a1, b1))
        lwork = _compute_lwork(hesvx_lw, n, lower)
        _, _, x, rcond, _, _, info = hesvx(a1, b1, lwork=lwork,
                                           lower=lower,
                                           overwrite_a=overwrite_a,
                                           overwrite_b=overwrite_b
                                           )
    else:
        posvx = get_lapack_funcs('posvx', (a1, b1))
        _, _, _, _, _, x, rcond, _, _, info = posvx(a1, b1,
                                                    lower=lower,
                                                    overwrite_a=overwrite_a,
                                                    overwrite_b=overwrite_b
                                                    )

    # Unlike ?xxSV, ?xxSVX writes the solution x to a separate array, and
    # overwrites b with its scaled version which is thrown away. Thus, the
    # solution does not admit the same shape with the original b. For
    # backwards compatibility, we reshape it manually.
    if b_is_1D:
        x = x.ravel()
    if b_is_ND:
        x = x.reshape(*b1.shape, order='F')

    if info < 0:
        raise ValueError('LAPACK reported an illegal value in {}-th argument'
                         '.'.format(-info))
    elif info == 0:
        return x
    elif 0 < info <= n:
        raise LinAlgError('Matrix is singular.')
    elif info > n:
        warnings.warn('scipy.linalg.solve\nIll-conditioned matrix detected.'
                      ' Result is not guaranteed to be accurate.\nReciprocal'
                      ' condition number: {}'.format(rcond), RuntimeWarning)
        return x
