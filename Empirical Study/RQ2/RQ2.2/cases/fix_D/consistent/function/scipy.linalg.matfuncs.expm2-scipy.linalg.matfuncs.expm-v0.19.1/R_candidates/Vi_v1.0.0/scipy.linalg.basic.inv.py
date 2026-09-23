def inv(a, overwrite_a=False, check_finite=True):
    """
    Compute the inverse of a matrix.

    Parameters
    ----------
    a : array_like
        Square matrix to be inverted.
    overwrite_a : bool, optional
        Discard data in `a` (may improve performance). Default is False.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    ainv : ndarray
        Inverse of the matrix `a`.

    Raises
    ------
    LinAlgError
        If `a` is singular.
    ValueError
        If `a` is not square, or not 2-dimensional.

    Examples
    --------
    >>> from scipy import linalg
    >>> a = np.array([[1., 2.], [3., 4.]])
    >>> linalg.inv(a)
    array([[-2. ,  1. ],
           [ 1.5, -0.5]])
    >>> np.dot(a, linalg.inv(a))
    array([[ 1.,  0.],
           [ 0.,  1.]])

    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square matrix')
    overwrite_a = overwrite_a or _datacopied(a1, a)
    #XXX: I found no advantage or disadvantage of using finv.
#     finv, = get_flinalg_funcs(('inv',),(a1,))
#     if finv is not None:
#         a_inv,info = finv(a1,overwrite_a=overwrite_a)
#         if info==0:
#             return a_inv
#         if info>0: raise LinAlgError, "singular matrix"
#         if info<0: raise ValueError('illegal value in %d-th argument of '
#                                     'internal inv.getrf|getri'%(-info))
    getrf, getri, getri_lwork = get_lapack_funcs(('getrf', 'getri',
                                                  'getri_lwork'),
                                                 (a1,))
    lu, piv, info = getrf(a1, overwrite_a=overwrite_a)
    if info == 0:
        lwork = _compute_lwork(getri_lwork, a1.shape[0])

        # XXX: the following line fixes curious SEGFAULT when
        # benchmarking 500x500 matrix inverse. This seems to
        # be a bug in LAPACK ?getri routine because if lwork is
        # minimal (when using lwork[0] instead of lwork[1]) then
        # all tests pass. Further investigation is required if
        # more such SEGFAULTs occur.
        lwork = int(1.01 * lwork)
        inv_a, info = getri(lu, piv, lwork=lwork, overwrite_lu=1)
    if info > 0:
        raise LinAlgError("singular matrix")
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal '
                         'getrf|getri' % -info)
    return inv_a
