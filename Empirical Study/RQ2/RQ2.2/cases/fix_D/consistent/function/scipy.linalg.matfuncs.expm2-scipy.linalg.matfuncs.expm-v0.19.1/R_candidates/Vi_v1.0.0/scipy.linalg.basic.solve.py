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
        If True, ``a^T x = b`` for real matrices, raises `NotImplementedError`
        for complex matrices (only for True).

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
    NotImplementedError
        If transposed is True and input a is a complex matrix.

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
    obtained via calling ?GESV, ?SYSV, ?HESV, and ?POSV routines of
    LAPACK respectively.
    """
    # Flags for 1D or nD right hand side
    b_is_1D = False

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

    # regularize 1D b arrays to 2D
    if b1.ndim == 1:
        if n == 1:
            b1 = b1[None, :]
        else:
            b1 = b1[:, None]
        b_is_1D = True

    # Backwards compatibility - old keyword.
    if sym_pos:
        assume_a = 'pos'

    if assume_a not in ('gen', 'sym', 'her', 'pos'):
        raise ValueError('{} is not a recognized matrix structure'
                         ''.format(assume_a))

    # Deprecate keyword "debug"
    if debug is not None:
        warnings.warn('Use of the "debug" keyword is deprecated '
                      'and this keyword will be removed in future '
                      'versions of SciPy.', DeprecationWarning)

    # Get the correct lamch function.
    # The LAMCH functions only exists for S and D
    # So for complex values we have to convert to real/double.
    if a1.dtype.char in 'fF':  # single precision
        lamch = get_lapack_funcs('lamch', dtype='f')
    else:
        lamch = get_lapack_funcs('lamch', dtype='d')

    # Currently we do not have the other forms of the norm calculators
    #   lansy, lanpo, lanhe.
    # However, in any case they only reduce computations slightly...
    lange = get_lapack_funcs('lange', (a1,))

    # Since the I-norm and 1-norm are the same for symmetric matrices
    # we can collect them all in this one call
    # Note however, that when issuing 'gen' and form!='none', then
    # the I-norm should be used
    if transposed:
        trans = 1
        norm = 'I'
        if np.iscomplexobj(a1):
            raise NotImplementedError('scipy.linalg.solve can currently '
                                      'not solve a^T x = b or a^H x = b '
                                      'for complex matrices.')
    else:
        trans = 0
        norm = '1'

    anorm = lange(norm, a1)

    # Generalized case 'gesv'
    if assume_a == 'gen':
        gecon, getrf, getrs = get_lapack_funcs(('gecon', 'getrf', 'getrs'),
                                               (a1, b1))
        lu, ipvt, info = getrf(a1, overwrite_a=overwrite_a)
        _solve_check(n, info)
        x, info = getrs(lu, ipvt, b1,
                        trans=trans, overwrite_b=overwrite_b)
        _solve_check(n, info)
        rcond, info = gecon(lu, anorm, norm=norm)
    # Hermitian case 'hesv'
    elif assume_a == 'her':
        hecon, hesv, hesv_lw = get_lapack_funcs(('hecon', 'hesv', 'hesv_lwork'),
                                                (a1, b1))
        lwork = _compute_lwork(hesv_lw, n, lower)
        lu, ipvt, x, info = hesv(a1, b1, lwork=lwork,
                                 lower=lower,
                                 overwrite_a=overwrite_a,
                                 overwrite_b=overwrite_b)
        _solve_check(n, info)
        rcond, info = hecon(lu, ipvt, anorm)
    # Symmetric case 'sysv'
    elif assume_a == 'sym':
        sycon, sysv, sysv_lw = get_lapack_funcs(('sycon', 'sysv', 'sysv_lwork'),
                                                (a1, b1))
        lwork = _compute_lwork(sysv_lw, n, lower)
        lu, ipvt, x, info = sysv(a1, b1, lwork=lwork,
                                 lower=lower,
                                 overwrite_a=overwrite_a,
                                 overwrite_b=overwrite_b)
        _solve_check(n, info)
        rcond, info = sycon(lu, ipvt, anorm)
    # Positive definite case 'posv'
    else:
        pocon, posv = get_lapack_funcs(('pocon', 'posv'),
                                       (a1, b1))
        lu, x, info = posv(a1, b1, lower=lower,
                           overwrite_a=overwrite_a,
                           overwrite_b=overwrite_b)
        _solve_check(n, info)
        rcond, info = pocon(lu, anorm)

    _solve_check(n, info, lamch, rcond)

    if b_is_1D:
        x = x.ravel()

    return x
