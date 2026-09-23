def solveh_banded(ab, b, overwrite_ab=False, overwrite_b=False, lower=False,
                    check_finite=True):
    """
    Solve equation a x = b. a is Hermitian positive-definite banded matrix.

    The matrix a is stored in `ab` either in lower diagonal or upper
    diagonal ordered form:

        ab[u + i - j, j] == a[i,j]        (if upper form; i <= j)
        ab[    i - j, j] == a[i,j]        (if lower form; i >= j)

    Example of `ab` (shape of a is (6,6), `u` =2)::

        upper form:
        *   *   a02 a13 a24 a35
        *   a01 a12 a23 a34 a45
        a00 a11 a22 a33 a44 a55

        lower form:
        a00 a11 a22 a33 a44 a55
        a10 a21 a32 a43 a54 *
        a20 a31 a42 a53 *   *

    Cells marked with * are not used.

    Parameters
    ----------
    ab : (`u` + 1, M) array_like
        Banded matrix
    b : (M,) or (M, K) array_like
        Right-hand side
    overwrite_ab : bool, optional
        Discard data in `ab` (may enhance performance)
    overwrite_b : bool, optional
        Discard data in `b` (may enhance performance)
    lower : bool, optional
        Is the matrix in the lower form. (Default is upper form)
    check_finite : boolean, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, K) ndarray
        The solution to the system a x = b.  Shape of return matches shape
        of `b`.

    """

    if check_finite:
        ab, b = map(np.asarray_chkfinite, (ab, b))
    else:
        ab, b = map(np.asarray, (ab,b))
    # Validate shapes.
    if ab.shape[-1] != b.shape[0]:
        raise ValueError("shapes of ab and b are not compatible.")

    pbsv, = get_lapack_funcs(('pbsv',), (ab, b))
    c, x, info = pbsv(ab, b, lower=lower, overwrite_ab=overwrite_ab,
                                            overwrite_b=overwrite_b)
    if info > 0:
        raise LinAlgError("%d-th leading minor not positive definite" % info)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal pbsv'
                                                                    % -info)
    return x
