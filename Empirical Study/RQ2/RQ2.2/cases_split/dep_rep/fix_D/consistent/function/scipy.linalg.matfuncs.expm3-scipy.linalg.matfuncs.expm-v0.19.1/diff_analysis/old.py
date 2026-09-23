def expm(A, q=None):
    """
    Compute the matrix exponential using Pade approximation.

    Parameters
    ----------
    A : (N, N) array_like or sparse matrix
        Matrix to be exponentiated.

    Returns
    -------
    expm : (N, N) ndarray
        Matrix exponential of `A`.

    References
    ----------
    .. [1] Awad H. Al-Mohy and Nicholas J. Higham (2009)
           "A New Scaling and Squaring Algorithm for the Matrix Exponential."
           SIAM Journal on Matrix Analysis and Applications.
           31 (3). pp. 970-989. ISSN 1095-7162

    Examples
    --------
    >>> from scipy.linalg import expm, sinm, cosm

    Matrix version of the formula exp(0) = 1:

    >>> expm(np.zeros((2,2)))
    array([[ 1.,  0.],
           [ 0.,  1.]])

    Euler's identity (exp(i*theta) = cos(theta) + i*sin(theta))
    applied to a matrix:

    >>> a = np.array([[1.0, 2.0], [-1.0, 3.0]])
    >>> expm(1j*a)
    array([[ 0.42645930+1.89217551j, -2.13721484-0.97811252j],
           [ 1.06860742+0.48905626j, -1.71075555+0.91406299j]])
    >>> cosm(a) + 1j*sinm(a)
    array([[ 0.42645930+1.89217551j, -2.13721484-0.97811252j],
           [ 1.06860742+0.48905626j, -1.71075555+0.91406299j]])

    """
    if q is not None:
        msg = "argument q=... in scipy.linalg.expm is deprecated." 
        warnings.warn(msg, DeprecationWarning)
    # Input checking and conversion is provided by sparse.linalg.expm().
    import scipy.sparse.linalg
    return scipy.sparse.linalg.expm(A)
