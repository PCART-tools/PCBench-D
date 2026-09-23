def cho_solve_banded(cb_and_lower, b, overwrite_b=False, check_finite=True):
    """Solve the linear equations A x = b, given the Cholesky factorization of A.

    Parameters
    ----------
    (cb, lower) : tuple, (array, bool)
        `cb` is the Cholesky factorization of A, as given by cholesky_banded.
        `lower` must be the same value that was given to cholesky_banded.
    b : array
        Right-hand side
    overwrite_b : bool, optional
        If True, the function will overwrite the values in `b`.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : array
        The solution to the system A x = b

    See also
    --------
    cholesky_banded : Cholesky factorization of a banded matrix

    Notes
    -----

    .. versionadded:: 0.8.0

    """
    (cb, lower) = cb_and_lower
    if check_finite:
        cb = asarray_chkfinite(cb)
        b = asarray_chkfinite(b)
    else:
        cb = asarray(cb)
        b = asarray(b)

    # Validate shapes.
    if cb.shape[-1] != b.shape[0]:
        raise ValueError("shapes of cb and b are not compatible.")

    pbtrs, = get_lapack_funcs(('pbtrs',), (cb, b))
    x, info = pbtrs(cb, b, lower=lower, overwrite_b=overwrite_b)
    if info > 0:
        raise LinAlgError("%d-th leading minor not positive definite" % info)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal pbtrs'
                         % -info)
    return x
