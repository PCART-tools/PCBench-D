def _cho_inv_batch(a, check_finite=True):
    """
    Invert the matrices a_i, using a Cholesky factorization of A, where
    a_i resides in the last two dimensions of a and the other indices describe
    the index i.

    Overwrites the data in a.

    Parameters
    ----------
    a : array
        Array of matrices to invert, where the matrices themselves are stored
        in the last two dimensions.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : array
        Array of inverses of the matrices ``a_i``.

    See also
    --------
    scipy.linalg.cholesky : Cholesky factorization of a matrix

    """
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if len(a1.shape) < 2 or a1.shape[-2] != a1.shape[-1]:
        raise ValueError('expected square matrix in last two dimensions')

    potrf, potri = get_lapack_funcs(('potrf','potri'), (a1,))

    tril_idx = np.tril_indices(a.shape[-2], k=-1)
    triu_idx = np.triu_indices(a.shape[-2], k=1)
    for index in np.ndindex(a1.shape[:-2]):

        # Cholesky decomposition
        a1[index], info = potrf(a1[index], lower=True, overwrite_a=False,
                                clean=False)
        if info > 0:
            raise LinAlgError("%d-th leading minor not positive definite"
                              % info)
        if info < 0:
            raise ValueError('illegal value in %d-th argument of internal'
                             ' potrf' % -info)
        # Inversion
        a1[index], info = potri(a1[index], lower=True, overwrite_c=False)
        if info > 0:
            raise LinAlgError("the inverse could not be computed")
        if info < 0:
            raise ValueError('illegal value in %d-th argument of internal'
                             ' potrf' % -info)

        # Make symmetric (dpotri only fills in the lower triangle)
        a1[index][triu_idx] = a1[index][tril_idx]

    return a1
