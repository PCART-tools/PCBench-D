def expm_cond(A, check_finite=True):
    """
    Relative condition number of the matrix exponential in the Frobenius norm.

    Parameters
    ----------
    A : 2d array-like
        Square input matrix with shape (N, N).
    check_finite : boolean, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    kappa : float
        The relative condition number of the matrix exponential
        in the Frobenius norm

    Notes
    -----
    A faster estimate for the condition number in the 1-norm
    has been published but is not yet implemented in scipy.

    .. versionadded:: 0.14.0

    See also
    --------
    expm : Compute the exponential of a matrix.
    expm_frechet : Compute the Frechet derivative of the matrix exponential.

    """
    if check_finite:
        A = np.asarray_chkfinite(A)
    else:
        A = np.asarray(A)
    if len(A.shape) != 2 or A.shape[0] != A.shape[1]:
        raise ValueError('expected a square matrix')

    X = scipy.linalg.expm(A)
    K = expm_frechet_kronform(A, check_finite=False)

    # The following norm choices are deliberate.
    # The norms of A and X are Frobenius norms,
    # and the norm of K is the induced 2-norm.
    A_norm = scipy.linalg.norm(A, 'fro')
    X_norm = scipy.linalg.norm(X, 'fro')
    K_norm = scipy.linalg.norm(K, 2)

    kappa = (K_norm * A_norm) / X_norm
    return kappa
