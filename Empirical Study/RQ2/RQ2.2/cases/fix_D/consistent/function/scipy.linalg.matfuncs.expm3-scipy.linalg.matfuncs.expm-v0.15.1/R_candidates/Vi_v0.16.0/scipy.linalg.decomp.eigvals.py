def eigvals(a, b=None, overwrite_a=False, check_finite=True):
    """
    Compute eigenvalues from an ordinary or generalized eigenvalue problem.

    Find eigenvalues of a general matrix::

        a   vr[:,i] = w[i]        b   vr[:,i]

    Parameters
    ----------
    a : (M, M) array_like
        A complex or real matrix whose eigenvalues and eigenvectors
        will be computed.
    b : (M, M) array_like, optional
        Right-hand side matrix in a generalized eigenvalue problem.
        If omitted, identity matrix is assumed.
    overwrite_a : bool, optional
        Whether to overwrite data in a (may improve performance)
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    w : (M,) double or complex ndarray
        The eigenvalues, each repeated according to its multiplicity,
        but not in any specific order.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge

    See Also
    --------
    eigvalsh : eigenvalues of symmetric or Hermitian arrays,
    eig : eigenvalues and right eigenvectors of general arrays.
    eigh : eigenvalues and eigenvectors of symmetric/Hermitian arrays.

    """
    return eig(a, b=b, left=0, right=0, overwrite_a=overwrite_a,
                check_finite=check_finite)
