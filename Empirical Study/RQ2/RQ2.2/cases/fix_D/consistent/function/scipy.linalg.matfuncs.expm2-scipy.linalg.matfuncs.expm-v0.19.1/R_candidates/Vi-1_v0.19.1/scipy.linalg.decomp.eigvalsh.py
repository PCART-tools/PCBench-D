def eigvalsh(a, b=None, lower=True, overwrite_a=False,
             overwrite_b=False, turbo=True, eigvals=None, type=1,
             check_finite=True):
    """
    Solve an ordinary or generalized eigenvalue problem for a complex
    Hermitian or real symmetric matrix.

    Find eigenvalues w of matrix a, where b is positive definite::

                      a v[:,i] = w[i] b v[:,i]
        v[i,:].conj() a v[:,i] = w[i]
        v[i,:].conj() b v[:,i] = 1


    Parameters
    ----------
    a : (M, M) array_like
        A complex Hermitian or real symmetric matrix whose eigenvalues and
        eigenvectors will be computed.
    b : (M, M) array_like, optional
        A complex Hermitian or real symmetric definite positive matrix in.
        If omitted, identity matrix is assumed.
    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of `a`. (Default: lower)
    turbo : bool, optional
        Use divide and conquer algorithm (faster but expensive in memory,
        only for generalized eigenvalue problem and if eigvals=None)
    eigvals : tuple (lo, hi), optional
        Indexes of the smallest and largest (in ascending order) eigenvalues
        and corresponding eigenvectors to be returned: 0 <= lo < hi <= M-1.
        If omitted, all eigenvalues and eigenvectors are returned.
    type : int, optional
        Specifies the problem type to be solved:

           type = 1: a   v[:,i] = w[i] b v[:,i]

           type = 2: a b v[:,i] = w[i]   v[:,i]

           type = 3: b a v[:,i] = w[i]   v[:,i]
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance)
    overwrite_b : bool, optional
        Whether to overwrite data in `b` (may improve performance)
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    w : (N,) float ndarray
        The N (1<=N<=M) selected eigenvalues, in ascending order, each
        repeated according to its multiplicity.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge,
        an error occurred, or b matrix is not definite positive. Note that
        if input matrices are not symmetric or hermitian, no error is reported
        but results will be wrong.

    See Also
    --------
    eigvals : eigenvalues of general arrays
    eigh : eigenvalues and right eigenvectors for symmetric/Hermitian arrays
    eig : eigenvalues and right eigenvectors for non-symmetric arrays

    """
    return eigh(a, b=b, lower=lower, eigvals_only=True,
                overwrite_a=overwrite_a, overwrite_b=overwrite_b,
                turbo=turbo, eigvals=eigvals, type=type,
                check_finite=check_finite)
