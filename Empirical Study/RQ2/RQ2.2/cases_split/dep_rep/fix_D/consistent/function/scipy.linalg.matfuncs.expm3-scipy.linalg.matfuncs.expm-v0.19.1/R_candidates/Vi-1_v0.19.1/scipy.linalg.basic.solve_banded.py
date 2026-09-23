def solve_banded(l_and_u, ab, b, overwrite_ab=False, overwrite_b=False,
                 debug=None, check_finite=True):
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
    overwrite_ab : bool, optional
        Discard data in `ab` (may enhance performance)
    overwrite_b : bool, optional
        Discard data in `b` (may enhance performance)
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, K) ndarray
        The solution to the system a x = b.  Returned shape depends on the
        shape of `b`.

    """

    # Deprecate keyword "debug"
    if debug is not None:
        warnings.warn('Use of the "debug" keyword is deprecated '
                      'and this keyword will be removed in the future '
                      'versions of SciPy.', DeprecationWarning)

    a1 = _asarray_validated(ab, check_finite=check_finite, as_inexact=True)
    b1 = _asarray_validated(b, check_finite=check_finite, as_inexact=True)
    # Validate shapes.
    if a1.shape[-1] != b1.shape[0]:
        raise ValueError("shapes of ab and b are not compatible.")
    (l, u) = l_and_u
    if l + u + 1 != a1.shape[0]:
        raise ValueError("invalid values for the number of lower and upper "
                         "diagonals: l+u+1 (%d) does not equal ab.shape[0] "
                         "(%d)" % (l+u+1, ab.shape[0]))

    overwrite_b = overwrite_b or _datacopied(b1, b)
    if a1.shape[-1] == 1:
        b2 = np.array(b1, copy=(not overwrite_b))
        b2 /= a1[1, 0]
        return b2
    if l == u == 1:
        overwrite_ab = overwrite_ab or _datacopied(a1, ab)
        gtsv, = get_lapack_funcs(('gtsv',), (a1, b1))
        du = a1[0, 1:]
        d = a1[1, :]
        dl = a1[2, :-1]
        du2, d, du, x, info = gtsv(dl, d, du, b1, overwrite_ab, overwrite_ab,
                                   overwrite_ab, overwrite_b)
    else:
        gbsv, = get_lapack_funcs(('gbsv',), (a1, b1))
        a2 = np.zeros((2*l+u+1, a1.shape[1]), dtype=gbsv.dtype)
        a2[l:, :] = a1
        lu, piv, x, info = gbsv(l, u, a2, b1, overwrite_ab=True,
                                overwrite_b=overwrite_b)
    if info == 0:
        return x
    if info > 0:
        raise LinAlgError("singular matrix")
    raise ValueError('illegal value in %d-th argument of internal '
                     'gbsv/gtsv' % -info)
