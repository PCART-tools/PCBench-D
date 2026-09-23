def cholesky_banded(ab, overwrite_ab=False, lower=False, check_finite=True):
    """
    Cholesky decompose a banded Hermitian positive-definite matrix

    The matrix a is stored in ab either in lower diagonal or upper
    diagonal ordered form::

        ab[u + i - j, j] == a[i,j]        (if upper form; i <= j)
        ab[    i - j, j] == a[i,j]        (if lower form; i >= j)

    Example of ab (shape of a is (6,6), u=2)::

        upper form:
        *   *   a02 a13 a24 a35
        *   a01 a12 a23 a34 a45
        a00 a11 a22 a33 a44 a55

        lower form:
        a00 a11 a22 a33 a44 a55
        a10 a21 a32 a43 a54 *
        a20 a31 a42 a53 *   *

    Parameters
    ----------
    ab : (u + 1, M) array_like
        Banded matrix
    overwrite_ab : bool, optional
        Discard data in ab (may enhance performance)
    lower : bool, optional
        Is the matrix in the lower form. (Default is upper form)
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    c : (u + 1, M) ndarray
        Cholesky factorization of a, in the same banded format as ab

    """
    if check_finite:
        ab = asarray_chkfinite(ab)
    else:
        ab = asarray(ab)

    pbtrf, = get_lapack_funcs(('pbtrf',), (ab,))
    c, info = pbtrf(ab, lower=lower, overwrite_ab=overwrite_ab)
    if info > 0:
        raise LinAlgError("%d-th leading minor not positive definite" % info)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal pbtrf'
                         % -info)
    return c
