def solve_banded(l_and_u, ab, b, overwrite_ab=False, overwrite_b=False,
                debug=False, check_finite=True):
    """
    Solve the equation a x = b for x, assuming a is banded matrix.

    The matrix a is stored in `ab` using the matrix diagonal ordered form::

        ab[u + i - j, j] == a[i,j]

    Example of `ab` (shape of a is (6,6), `u` =1, `l` =2)::

        *    a01  a12  a23  a34  a45
        a00  a11  a22  a33  a44  a55
        a10  a21  a32  a43  a54   *
        a20  a31  a42  a53   *    *

    Parameters
    ----------
    (l, u) : (integer, integer)
        Number of non-zero lower and upper diagonals
    ab : (`l` + `u` + 1, M) array_like
        Banded matrix
    b : (M,) or (M, K) array_like
        Right-hand side
    overwrite_ab : boolean, optional
        Discard data in `ab` (may enhance performance)
    overwrite_b : boolean, optional
        Discard data in `b` (may enhance performance)
    check_finite : boolean, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, K) ndarray
        The solution to the system a x = b.  Returned shape depends on the
        shape of `b`.

    """
    (l, u) = l_and_u
    if check_finite:
        a1, b1 = map(np.asarray_chkfinite, (ab, b))
    else:
        a1, b1 = map(np.asarray, (ab,b))
    # Validate shapes.
    if a1.shape[-1] != b1.shape[0]:
        raise ValueError("shapes of ab and b are not compatible.")
    if l + u + 1 != a1.shape[0]:
        raise ValueError("invalid values for the number of lower and upper diagonals:"
                " l+u+1 (%d) does not equal ab.shape[0] (%d)" % (l+u+1, ab.shape[0]))

    overwrite_b = overwrite_b or _datacopied(b1, b)

    gbsv, = get_lapack_funcs(('gbsv',), (a1, b1))
    a2 = np.zeros((2*l+u+1, a1.shape[1]), dtype=gbsv.dtype)
    a2[l:,:] = a1
    lu, piv, x, info = gbsv(l, u, a2, b1, overwrite_ab=True,
                                                overwrite_b=overwrite_b)
    if info == 0:
        return x
    if info > 0:
        raise LinAlgError("singular matrix")
    raise ValueError('illegal value in %d-th argument of internal gbsv' % -info)
